# Game Design Specification: Paper Warfire (GAME_DESIGN.md)

Dokumen ini mendefinisikan aturan permainan mendalam, siklus fase WEGO, progresi giliran, sistem ekonomi koin, dan balancing taktis **Paper Warfire**.

---

## 1. Aturan Dasar Permainan & Filosofi Desain

Paper Warfire dibangun di atas premis: **"Keputusan taktis di bawah kabut ketidakpastian"**. Pemain tidak dituntut memiliki refleks tangan cepat, melainkan kemampuan membaca posisi lawan, mengelola jangkauan senjata, serta meramalkan manuver musuh.

### Pilar Mekanik Inti:
1. **Siklus WEGO (Command Planning & Simultaneous Execution):**
   - Kedua pihak menyusun perintah secara rahasia pada fase yang sama.
   - Tidak ada tembakan atau langkah instan selama perencanaan; semua aksi dikunci hingga kedua pihak menyatakan `READY`.
2. **Keterbatasan Informasi (Fog of War):**
   - Tile medan perang memiliki 3 status visibilitas:
     - `UNEXPLORED` (Hitam pekat/gelap total): Belum pernah dikunjungi atau diintai.
     - `EXPLORED / FOGGED` (Redup/semi-transparan): Terrain terlihat, tetapi unit lawan yang bersembunyi di dalamnya tidak terlihat.
     - `VISIBLE` (Terang penuh): Sedang berada dalam radius pandang unit aktif atau baru terkena dampak ledakan.
3. **Serangan Berbasis Koordinat Manual:**
   - Pemain memasukkan atau mengklik koordinat target (misal: `X: 12, Y: 8` atau `H8`).
   - Senjata memiliki area dampak (AoE). Serangan yang meleset dari unit target tetap berguna untuk mengungkap area kabut perang di sekitarnya.

---

## 2. Siklus Fase Pertandingan (Match Phase Loop)

Setiap giliran (*turn*) dalam pertandingan terdiri dari 4 sub-fase yang berjalan berurutan:

```text
[AWAL GILIRAN]
       |
       v
+-------------------------------------------------------------+
| 1. PLANNING PHASE (Fase Perencanaan)                        |
| - Pemain memilih unit dan menetapkan 1 aksi (MOVE / ATTACK) |
| - AI menyusun perintah secara otonom di latar belakang       |
| - Perintah disimpan dalam antrean (Command Queue)           |
| - Diakhiri saat pemain menekan [READY / END PLANNING]       |
+-------------------------------------------------------------+
       |
       v
+-------------------------------------------------------------+
| 2. WAR PHASE (Fase Eksekusi Simultan)                       |
| - Step 1: Unit bergerak serentak ke koordinat tujuan        |
| - Step 2: Radius pandang diperbarui                         |
| - Step 3: Seluruh tembakan & artileri ditembakkan serentak  |
| - Step 4: Kerusakan dihitung & unit HP <= 0 dieliminasi     |
| - Step 5: Area dampak tembakan mengungkap Fog of War        |
+-------------------------------------------------------------+
       |
       v
+-------------------------------------------------------------+
| 3. TURN EVALUATION & REWARD PHASE                           |
| - Menghitung perolehan koin giliran                         |
| - Memeriksa kondisi Menang / Kalah                          |
| - Akses menu Upgrade unit (opsional per giliran)            |
+-------------------------------------------------------------+
       |
       v
[Kondisi Selesai?] ──Ya──► [VICTORY / DEFEAT SCREEN]
       | Tidak
       v
[Giliran Bertambah (Turn + 1)] ──► Kembali ke PLANNING PHASE
```

---

## 3. Syarat Menang & Kalah (Win / Lose Conditions)

- **Syarat Menang Mutlak (Victory):**
  - Seluruh unit lawan berhasil dieliminasi (Total Enemy Units = 0).
  - *Atau (Mode Objektif Opsional):* Menguasai tile pusat markas musuh (*Command Post*) selama 2 giliran berturut-turut.
- **Syarat Kalah Mutlak (Defeat):**
  - Seluruh unit milik pemain musnah (Total Player Units = 0).
  - *Atau:* Gagal mengeliminasi musuh sebelum batas maksimal giliran tercapai (*Max Turn Limit = 25 Turns*).

---

## 4. Sistem Ekonomi Koin & Upgrade

Setelah setiap War Phase berakhir, pemain memperoleh koin berdasarkan kontribusi pertempuran pada giliran tersebut:

### A. Sumber Pendapatan Koin:
- **Base Turn Income:** +50 Koin per giliran (dana operasional).
- **Eliminasi Unit Lawan:**
  - Infanteri (Pistol): +25 Koin
  - Machine Gun / Sniper: +40 Koin
  - Tank / Mortar / Artillery: +75 Koin
- **Pengungkapan Tile Baru (Recon Bonus):** +1 Koin per tile kabut perang baru yang berhasil dibuka.

### B. Menu Peningkatan Kemampuan (Unit Upgrades):
Koin dapat dibelanjakan selama fase evaluasi untuk memperkuat pasukan:
| Nama Upgrade | Biaya Koin | Efek Mekanik | Unit yang Berhak |
| :--- | :--- | :--- | :--- |
| **Penetration Shells** | 120 Koin | Meningkatkan damage dasar sebesar $+15\%$ | Tank, Artillery, Sniper |
| **Extended Optics / Scope** | 100 Koin | Menambah jangkauan tembak $+2$ tile dan jarak pandang $+1$ tile | Sniper, Pistol, Machine Gun |
| **High-Capacity Magazine** | 90 Koin | Mengurangi penalti falloff damage di tile tepi AoE | Machine Gun, Mortar |
| **Scan Location Drone** | 80 Koin | Item sekali pakai: membuka area 5x5 tile di koordinat mana pun | Komando Pemain (Global) |

---

## 5. Pembangkitan Medan Perang (Procedural Battlefield Grid)

- **Ukuran Grid Standar:** $24 \times 16$ tile (rasio layar 3:2 pada resolusi HD).
- **Pembagian Zona Awal:**
  - **Sisi Kiri (Kolom 1 - 4):** Zona penempatan awal pasukan Pemain.
  - **Sisi Tengah (Kolom 5 - 20):** Zona netral tak bertuan dengan rintangan acak dan kabut Fog of War tebal.
  - **Sisi Kanan (Kolom 21 - 24):** Zona penempatan awal pasukan Lawan (AI).
- **Jenis Terrain & Pengaruh Taktis:**
  - **Plains / Grass (Netral):** Biaya gerak 1 tile, damage modifier $1.0\times$.
  - **Forest / Trees (Cover):** Biaya gerak 2 tile, damage modifier $0.8\times$ (mitigasi 20%), menghalangi pandangan lurus.
  - **Mountain / Rocks (Benteng):** Tidak dapat dilalui unit darat biasa (*impassable*), damage modifier $0.6\times$, dapat dilompati artileri.
  - **Water / Swamp (Bahaya):** Biaya gerak 2 tile, damage modifier $1.2\times$ (unit lebih rentan).
