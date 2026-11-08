# Spesifikasi Tampilan Heads-Up Display (hud.md)

Dokumen ini mendefinisikan rancangan layout, keterbacaan data taktis, panel perintah unit, indikator fase pertempuran, dan sistem umpan balik antarmuka (*UI Feedback*) pada **Paper Warfire** (Tanggung Jawab Role 3).

---

## 1. Arsitektur Layout Layar In-Game (HUD Architecture)

Layar gameplay beresolusi $1280 \times 720$ piksel dibagi menjadi 3 zona visual utama untuk memastikan seluruh informasi penting terbaca tanpa mengganggu area pertempuran:

```text
+----------------------------------------------------------------------------------------------------+
| [BAR ATAS - STATUS PERTANDINGAN]                                                                    |
| PAPER WARFIRE | TURN: 04 | PHASE: [ PLANNING PHASE ] | KOIN: 250 | UNIT AKTIF: 5/6 | SISA MUSUH: 4  |
+----------------------------------------------------+-----------------------------------------------+
|                                                    | [PANEL KANAN - KONTROL & DETAIL TAKTIS]       |
|                                                    | +-------------------------------------------+ |
|                                                    | | INFORMASI UNIT TERPILIH                   | |
|                                                    | | [Icon] TANK UNIT                          | |
|                                                    | | HP: [████████████░░░░] 160 / 200          | |
|                   BATTLEFIELD                      | | Move: 3 tile | Attack: 15 tile (AoE 3x3)  | |
|                                                    | | Status: Belum Diberi Aksi                 | |
|              [GRID MEDAN PERANG]                   | +-------------------------------------------+ |
|             (Ukuran: 24 x 16 Tile)                 | | PILIH PERINTAH UNIT                       | |
|                                                    | | [ MOVE ]       [ ATTACK ]      [ SCAN ]   | |
|                                                    | +-------------------------------------------+ |
|                                                    | | INPUT KOORDINAT MANUAL                    | |
|                                                    | | TARGET TILE: X: [ 14 ]  Y: [ 08 ] (H8)    | |
|                                                    | | [ BATALKAN ]        [ KONFIRMASI AKSI ]   | |
|                                                    | +-------------------------------------------+ |
|                                                    | | DAFTAR PERINTAH SIAP EKSEKUSI             | |
|                                                    | | 1. Pistol   -> MOVE ke D5                 | |
|                                                    | | 2. Sniper   -> ATTACK ke H8               | |
|                                                    | | 3. Tank     -> ATTACK ke K10              | |
|                                                    | | [HAPUS SEMUA]       [READY / SELESAI]     | |
+----------------------------------------------------+-----------------------------------------------+
| [BAR BAWAH] PANDUAN KONTROL: [L-CLICK] Pilih/Target | [WASD/Scroll] Geser Kamera | [ESC] Jeda Menu  |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Rincian Komponen HUD

### A. Bar Status Atas (Top Match Header)
- **Turn Counter:** Menampilkan nomor giliran saat ini (misal: `TURN: 04 / 25`).
- **Phase Banner:** 
  - Saat `Planning Phase`: Berwarna **Kuning Keemasan (#F2C14E)** dengan teks *"PLANNING PHASE - Susun Perintah Pasukan"*.
  - Saat `War Phase`: Berwarna **Merah Peringatan (#E05252)** dengan teks *"WAR PHASE - Mengeksekusi Perintah Simultan..."*.
- **Indikator Ekonomi (Coin Wallet):** Ikon koin emas diikuti saldo numerik (misal: `250`).
- **Unit Counter:** Menampilkan jumlah unit kawan yang masih bertempur vs perkiraan sisa unit lawan yang diketahui.

### B. Panel Samping Informasi Unit (Unit Inspector Panel)
Ketika pemain mengklik salah satu unit di medan perang:
- **Ikon & Nama Unit:** Menampilkan simbol taktis geometris dan nama kelas unit.
- **Health Bar Progresif:** Batang visual dengan kode warna adaptif (Hijau $>50\%$, Kuning $25-50\%$, Merah $\le 25\%$).
- **Statistik Tempur:** Jarak tempuh (*Move Range*), jangkauan senjata (*Attack Range*), jenis area dampak (*Single Tile* atau *Area 3x3*).
- **Status Tindakan:** Menampilkan label apakah unit sudah menerima perintah di giliran ini atau belum.

### C. Panel Input & Validasi Koordinat (Targeting Panel)
- Pemain memasukkan koordinat sasaran secara manual melalui kotak input teks pada panel samping (misal: input kolom X dan baris Y, atau notasi alfanumerik `H8`). Penargetan sengaja dirancang tanpa klik langsung pada medan perang untuk mempertegas nuansa permainan perang kertas dan strategi koordinat buta.
- **Validasi Instan:**
  - Jika koordinat sah: Kotak berbingkai **Hijau (#536B4F)**, tombol *Konfirmasi Aksi* menyala aktif.
  - Jika koordinat di luar jangkauan: Kotak berbingkai **Merah (#E05252)**, muncul teks error kecil *"Di luar jangkauan tembak!"*, tombol konfirmasi nonaktif.

### D. Panel Antrean Perintah (Command Queue List)
- Menampilkan daftar ringkas semua unit yang telah diberi perintah.
- Pemain dapat mengklik ikon silang di samping perintah untuk membatalkan (*undo/remove*) perintah unit tertentu sebelum menekan tombol utama `[READY / SELESAI]`.

---

## 3. Desain Keterbacaan Visual & Feedback (UX Alignment)

Memenuhi **Rubrik Penilaian UX (Bab 4)**:
1. **Kejelasan Status Fase (Objective Clarity):**
   - Transisi antara fase perencanaan dan eksekusi ditandai dengan perubahan banner atas dan suara klakson militer singkat.
2. **Keterbacaan Medan (Visual Readability):**
   - Garis grid abu-abu netral (`#555B66`) memperjelas batas tile.
   - Tile yang tertutup Fog of War dibuat gelap pekat (`#17191F`) agar pemain langsung mengetahui area yang belum diintai.
   - Tile terpilih diberi garis tepi kuning terang (`#F2C14E`) tebal 2 piksel.
3. **Umpan Balik Tindakan (Action Feedback):**
   - Mengklik tombol memutar SFX klik taktil lembut.
   - Konfirmasi perintah menampilkan garis putus-putus ke target pada layar grid.
   - Saat War Phase, damage memunculkan angka beterbangan (*floating text*) dan animasi guncangan layar (*screen shake*) ringan saat artileri meledak.
