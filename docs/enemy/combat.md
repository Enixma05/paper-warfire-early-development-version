# Spesifikasi Tempur & Damage Lawan (combat.md)

Dokumen ini mendefinisikan karakteristik tempur unit lawan, parameter statistik (HP, Damage, Range, Footprint), mekanisme kalkulasi kerusakan, aturan area dampak (AoE), serta resolusi benturan dalam sistem pertempuran **Paper Warfire**.

---

## 1. Tabel Parameter Statistik Unit Tempur Lawan

Seluruh unit musuh memiliki atribut dasar yang seimbang dengan unit pemain, dengan peran dan spesialisasi taktis yang berbeda:

| Jenis Unit | HP Maksimal | Move Range (Tile) | Attack Range (Tile) | Base Damage | Area of Effect (AoE) | Ukuran (Footprint) | Peran Taktis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Pistol Unit** | 70 HP | 4 tile | 6 tile | 25 DMG | Single Tile (1x1) | 1x1 tile | Infanteri serbaguna, pengintai garis depan, biaya rendah |
| **Machine Gun** | 90 HP | 3 tile | 8 tile | 20 DMG | Area 3x3 tile | 1x1 tile | Supresi area, mengancam formasi kelompok unit pemain |
| **Sniper Unit** | 60 HP | 2 tile | 12 tile | 60 DMG | Single Tile (1x1) | 1x1 tile | *High single-target burst*, eliminasi unit prioritas |
| **Tank Unit** | 200 HP | 3 tile | 15 tile | 50 DMG | Area 3x3 tile | 2x3 tile | Benteng garis depan (*heavy vanguard*), perusak konsentrasi |
| **Mortar Unit** | 100 HP | 2 tile | 18 tile | 40 DMG | Area 3x3 tile | 1x2 tile | Artileri menengah, tembakan parabola melompati rintangan |
| **Artillery Unit**| 120 HP | 1 tile | 25 tile | 75 DMG | Area 3x3 tile | 2x2 tile | *Long-range siege*, penguasa medan dan pembuka kabut perang |
| **Grenade Attack**| - | Khusus | 5 tile | 50 DMG | Area 3x3 tile | - | Serangan jarak pendek berdaya ledak tinggi |

---

## 2. Model Kalkulasi Kerusakan (Damage Calculation Model)

Perhitungan kerusakan pada **War Phase** diproses berdasarkan formula:

$$\text{Final Damage} = \text{Base Damage} \times \text{Distance Falloff Multiplier} \times \text{Terrain Defense Multiplier} \times \text{Upgrade Modifier}$$

### A. Komponen Formula:
1. **Distance Falloff (Untuk Serangan Area 3x3):**
   - **Pusat Titik Koordinat (Center Tile):** $100\%$ Base Damage.
   - **Tile Sekitar Pusat (Surrounding 8 Tiles):** $50\%$ Base Damage.
2. **Terrain Defense Multiplier:**
   - **Open Ground / Rumput:** $1.0\times$ (Kerusakan penuh).
   - **Forest / Rindang:** $0.8\times$ (Memberikan cover 20% mitigasi damage).
   - **Rocky / Benteng:** $0.6\times$ (Memberikan cover 40% mitigasi damage).
   - **Water / Rawa:** $1.2\times$ (Unit terjebak menerima ekstra 20% damage).
3. **Upgrade Modifier:**
   - Unit yang telah mendapatkan *Penetration Upgrade* menaikkan base multiplier sebesar $+15\%$.

---

## 3. Resolusi Pertempuran WEGO (Simultaneous Resolution Logic)

Dalam sistem WEGO, kedua pihak mengeksekusi perintah pada fase yang sama. Untuk menjaga konsistensi dan keadilan permainan, sistem resolusi mengikuti urutan berikut pada **War Phase**:

```text
[Urutan Resolusi War Phase]
1. Tahap Gerak (Movement Phase):
   Semua unit yang memiliki perintah MOVE berpindah ke koordinat tujuan.
   - Jika dua unit menuju tile yang sama: Resolusi Tabrakan (Clash/Cancel).
   - Tile tujuan diverifikasi terhadap terrain yang impassable.
   
2. Tahap Pengintaian (Recon/Vision Phase):
   Area pandang diperbarui berdasarkan posisi baru unit setelah bergerak.

3. Tahap Eksekusi Serangan (Combat/Firing Phase):
   Semua unit yang memiliki perintah ATTACK melepaskan tembakan ke koordinat target.
   - Pengecekan koordinat: Apakah peluru/proyektil jatuh pada tile yang ada unitnya?
   - Jika unit target sudah bergerak keluar dari tile sebelum serangan jatuh:
     Tembakan dianggap MISSED (kecuali terkena radius AoE 3x3).
   - Pengurangan HP dihitung secara bersamaan (simultaneous damage application).

4. Tahap Pembaruan Eliminasi (Casualty Resolution):
   Unit yang memiliki HP <= 0 diubah statusnya menjadi DESTROYED.
   - Memutar SFX ledakan/hancur dan partikel visual.
   - Drop koin dihitung dan ditambahkan ke inventaris pihak yang mengeliminasi.

5. Tahap Pengungkapan Fog of War (Impact Reveal):
   Semua titik dampak tembakan dan ledakan mengungkap tile di sekitarnya.
```

---

## 4. Mekanisme Penerimaan Kerusakan Lawan (Enemy Take Damage)

Ketika unit musuh terkena serangan dari pemain:
1. **Pemeriksaan Health:**
   ```python
   def take_damage(self, amount: int, attacker_source: Unit) -> None:
       self.current_hp = max(0, self.current_hp - amount)
       self.trigger_damage_effect() # Kedip putih / shake animasi visual
       
       if self.current_hp == 0:
           self.is_alive = False
           self.trigger_death_sequence(attacker_source)
   ```
2. **Feedback Visual & Audio:**
   - **Visual:** Sprite unit berkedip (*flash white/red*) selama 0.15 detik, memunculkan angka kerusakan (*floating combat text*), dan bar HP di atas unit diperbarui secara halus.
   - **Audio:** SFX hantaman proyektil/ledakan berbunyi sesuai jenis senjata penyerang.
3. **Reward & Skor Kemenangan:**
   - Setiap unit musuh yang berhasil dieliminasi memberikan koin kepada pemain:
     - Minion/Pistol: +25 Koin
     - Machine Gun / Sniper: +40 Koin
     - Tank / Mortar / Artillery: +75 Koin
   - Mengurangi counter unit lawan aktif pada HUD (`Enemy Units Remaining`).
