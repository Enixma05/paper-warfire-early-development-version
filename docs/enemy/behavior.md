# Spesifikasi Perilaku & AI Lawan (behavior.md)

Dokumen ini mendefinisikan arsitektur kecerdasan buatan (*Rule-Based AI*), mesin status (*State Machine*), pemrosesan keterbatasan informasi (*Fog of War Awareness*), serta hierarki pengambilan keputusan taktis lawan pada **Paper Warfire**.

---

## 1. Arsitektur AI: Rule-Based WEGO System

Dalam Paper Warfire, lawan (AI) tidak bertindak secara instan maupun bergerak real-time, melainkan menyusun perencanaan perintah pada **Planning Phase** bersamaan dengan pemain, yang kemudian dieksekusi serentak pada **War Phase**.

### Prinsip Utama AI:
1. **Fog of War Compliance (No Cheating):**
   - AI **dilarang keras** membaca langsung koordinat unit pemain yang berada di balik kabut Fog of War (`tile.is_visible_to_enemy == False`).
   - AI hanya boleh mengambil keputusan berdasarkan:
     - Posisi unit pemain yang sedang berada di area pandang (*currently visible*).
     - Riwayat posisi terakhir pemain yang pernah terungkap (*last known position memory*).
     - Titik asal tembakan atau dampak ledakan yang baru terjadi.
2. **One Main Command per Unit:**
   - Setiap unit AI dalam satu giliran hanya dapat memilih satu perintah utama: `MOVE` atau `ATTACK` (atau `SCAN` jika unit memiliki kemampuan intelijen).
3. **Koordinasi Pasukan Komprehensif:**
   - AI mengevaluasi peran taktis unit (Pistol/Machine Gun sebagai garis depan, Sniper/Tank/Mortar/Artillery sebagai lini tengah dan pendukung tembakan jarak jauh).

---

## 2. Model Pengetahuan AI (AI Knowledge & Memory Model)

Untuk mematuhi batasan Fog of War, AI mengelola struktur data memori lokal setiap giliran:

```text
AIBattlefieldMemory:
  - visible_player_units: List[UnitInfo]        # Unit pemain yang saat ini terlihat
  - last_known_positions: Dict[UnitID, TilePos] # Koordinat terakhir & giliran tercatat
  - suspected_clusters: List[TilePos]           # Titik kemungkinan konsentrasi lawan
  - danger_map: GridMap[Float]                  # Heatmap ancaman tembakan pemain
  - strategic_waypoints: List[TilePos]          # Posisi choke point / tengah peta
```

### Mekanisme Pembaruan Memori:
- **Scan & Sight Range:** Pada awal Planning Phase, setiap unit musuh memeriksa area pandangnya (*vision range*). Jika ada unit pemain dalam radius, perbarui `visible_player_units`.
- **Dampak Serangan:** Jika musuh terkena serangan dari area tak terlihat, tandai koordinat dampak dan radius senjata tersebut ke dalam `suspected_clusters`.
- **Decay Memory:** Posisi pemain pada `last_known_positions` memiliki bobot keyakinan yang menurun seiring bertambahnya giliran jika unit tersebut tidak lagi terlihat.

---

## 3. Finite State Machine (FSM) Pengambilan Keputusan AI

AI beroperasi melalui evaluasi status global per giliran dan status individual per unit:

```text
                  +-----------------------+
                  |     EVALUATE STATE    |
                  |  (Cek Memori & Medan) |
                  +-----------+-----------+
                              |
            +-----------------+-----------------+
            |                                   |
            v                                   v
   [Ada Target Terlihat /              [Tidak Ada Target
      Posisi Diketahui]                  Terlihat di Radar]
            |                                   |
            v                                   v
   +-----------------+                 +-----------------+
   |   COMBAT MODE   |                 |   SEARCH MODE   |
   +--------+--------+                 +--------+--------+
            |                                   |
   +--------+--------+                 +--------+--------+
   | - Target Prioritizing             | - Advance to Waypoint
   | - In-Range? -> ATTACK             | - Flank Choke Point
   | - Out-Range? -> MOVE to Range     | - Blind Fire / Area Bombard
   | - Danger High? -> TACTICAL RETREAT| - Recon / Scan Unrevealed
   +-----------------+                 +-----------------+
```

### A. State: SEARCH & PATROL (Pencarian Area)
- **Kondisi:** `visible_player_units` kosong dan tidak ada riwayat baru.
- **Logika Perintah:**
  - **Unit Cepat/Garis Depan (Pistol, Machine Gun):** Diberi perintah `MOVE` maju menyisir menuju garis tengah peta (*strategic waypoints*) atau choke point alami untuk membuka kabut perang.
  - **Unit Artileri/Jarak Jauh (Mortar, Artillery, Tank):** Melakukan pergerakan bertahap mencari posisi aman atau melakukan *blind bombardment* ke koordinat choke point yang dicurigai.

### B. State: COMBAT ENGAGEMENT (Pertempuran Aktif)
- **Kondisi:** Minimal satu unit pemain teridentifikasi dalam jarak jangkau atau jarak gerak.
- **Logika Perintah:**
  1. **Evaluasi Target (Priority Scoring):**
     $$\text{Score} = (\text{Base Priority}) + (100 - \text{Target HP}) + (\text{Threat Factor}) - (\text{Distance} \times 2)$$
     - Unit bernilai tinggi seperti Sniper atau Artileri pemain mendapat prioritas lebih tinggi.
     - Unit dengan sisa HP rendah diprioritaskan untuk dieliminasi (*finishing blow*).
  2. **Penentuan Tindakan:**
     - Jika target berada dalam `Attack Range` senjata unit: Buat perintah `ATTACK` ke koordinat target.
     - Jika target di luar `Attack Range` tetapi bisa didekati: Buat perintah `MOVE` ke tile terdekat yang memenuhi syarat jangkauan tembak.
     - Jika unit terluka parah (HP kritis) dan berhadapan dengan unit kuat: Ambil opsi `MOVE` mundur ke balik rintangan terrain.

### C. State: BLIND BOMBARDMENT & PREDICTION (Prediksi Serangan Koordinat)
- **Kondisi:** Target menghilang ke dalam Fog of War pada giliran sebelumnya.
- **Logika Perintah:**
  - Unit area seperti **Machine Gun**, **Mortar**, dan **Artillery** memilih koordinat target di sekitar `last_known_position` dengan memperhitungkan radius gerak maksimum pemain dalam 1 giliran.
  - Area 3x3 dari Mortar/Artillery dimanfaatkan untuk memaksimalkan peluang mengenai pemain sekaligus membuka kembali Fog of War di titik tersebut.

---

## 4. Alur Algoritma Penyusunan Perintah AI (Planning Phase Pipeline)

Pada setiap giliran di fase perencanaan, modul AI (`EnemyAIController`) menjalankan tahapan berikut:

```python
def plan_enemy_turn(battlefield, enemy_units, ai_memory):
    # 1. Perbarui persepsi kabut perang
    ai_memory.update_vision(battlefield, enemy_units)
    
    # 2. Urutkan unit berdasarkan peran taktis (Artileri -> Sniper -> Tank -> Infanteri)
    sorted_units = prioritize_unit_execution_order(enemy_units)
    
    orders = []
    occupied_target_tiles = set()
    
    for unit in sorted_units:
        # Cek apakah unit dapat menyerang target yang valid
        best_target = evaluate_attack_targets(unit, ai_memory, occupied_target_tiles)
        if best_target:
            order = Command(type=CommandType.ATTACK, unit=unit, target_coord=best_target.coord)
            orders.append(order)
            continue
            
        # Jika tidak menyerang, tentukan pergerakan taktis terbaik
        best_destination = evaluate_move_destination(unit, battlefield, ai_memory)
        if best_destination:
            order = Command(type=CommandType.MOVE, unit=unit, target_coord=best_destination)
            orders.append(order)
            occupied_target_tiles.add(best_destination)
            
    return orders
```

---

## 5. Hubungan State AI dengan Siklus Game Utama

| Fase Game | Aktivitas Modul AI (`src/enemy/`) |
| :--- | :--- |
| **PLANNING_PHASE** | Menghitung bobot target, memvalidasi aturan FoW, menghasilkan antrean perintah AI (`enemy_orders`), dan mengirim sinyal `READY`. |
| **WAR_PHASE** | Pasif menerima eksekusi resolusi dari `GameBattleResolver`. Menerima pembaruan HP jika terkena serangan pemain. |
| **TURN_EVALUATION** | Menerima koin hasil giliran, mengalokasikan upgrade unit (jika mode upgrade aktif), dan mereset status kesiapan giliran. |
