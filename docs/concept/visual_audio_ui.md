# Konsep Visual, Audio & Antarmuka Pengguna (Audio-Visual & UX Canvas)

## 1. Panduan Arah Seni Visual (Art Style)

**Gaya Grafis:**

Paper Warfire menggunakan gaya *Geometric Minimalist 2D* dengan perspektif top-down. Unit, terrain, dan objek medan perang direpresentasikan melalui bentuk geometris sederhana agar mudah dikenali tanpa memerlukan aset visual yang kompleks. Gaya ini terinspirasi dari permainan perang menggunakan kertas, dengan penekanan pada keterbacaan posisi unit, koordinat grid, dan informasi taktis. Tampilan dikembangkan menggunakan Godot Engine dengan GDScript.

**Palet Warna Dominan:**

- Background: Abu-abu gelap kebiruan (#252830) untuk area antarmuka dan latar medan perang.
- Grid: Abu-abu netral (#555B66) untuk garis pembatas tile.
- Player: Biru (#4A90E2) untuk membedakan unit pemain dari pihak lawan.
- Musuh: Merah (#E05252) untuk menandai unit lawan yang telah teridentifikasi.
- Terrain: Hijau kusam (#536B4F), cokelat (#806548), dan abu-abu (#777D85) untuk membedakan jenis medan.
- Elemen Interaktif: Kuning keemasan (#F2C14E) untuk tile terpilih, koordinat target, dan indikator perintah.
- Fog of War: Abu-abu sangat gelap (#17191F) untuk area yang belum diketahui atau belum terlihat.
- Informasi Pendukung: Putih keabu-abuan (#E5E7EB) untuk teks dan informasi umum.

**Keterbacaan Visual (UX):**

Pembedaan unit menggunakan kombinasi warna, ikon, bentuk, dan penanda kepemilikan sehingga tidak hanya bergantung pada warna. Unit pemain ditandai dengan warna biru, sedangkan unit musuh menggunakan warna merah ketika teridentifikasi. Tile yang dipilih diberi garis tepi kuning, sementara tile tujuan pergerakan dan koordinat serangan menggunakan simbol atau penanda khusus.

Area Fog of War dibuat lebih gelap dibandingkan tile yang telah diketahui. Informasi musuh yang tidak terlihat tidak ditampilkan secara langsung, sedangkan posisi terakhir yang diketahui dapat ditandai secara terpisah jika mekanik tersebut diterapkan. Indikator jangkauan gerak, jangkauan serangan, dan area dampak serangan menggunakan pola atau warna yang berbeda agar pemain dapat membedakannya dengan cepat.

## 2. Layout Antarmuka Pengguna (UI Wireframe Sketch)

### A. HUD In-Game (Saat Bermain)

```text
+------------------------------------------------------------------+
| PAPER WARFIRE                 TURN: 05        PHASE: PLANNING     |
+------------------------------------------------------------------+
| KOIN: 250      UNIT AKTIF: 5/7       WAKTU: 00:45                |
+--------------------------+---------------------------------------+
| INFORMASI UNIT           |                                       |
| Nama: Sniper             |                                       |
| HP: 80/100               |                                       |
| Move Range: 4            |             BATTLEFIELD                |
| Attack Range: 12          |                                       |
| Status: Belum Diberi Aksi |          [GRID DAN UNIT]               |
|                          |                                       |
| [MOVE] [ATTACK] [SCAN]    |                                       |
+--------------------------+---------------------------------------+
| PERINTAH UNIT            | KOORDINAT TARGET: [ H8 ] [CONFIRM]    |
| 1. Pistol - Move C5      |                                       |
| 2. Sniper - Attack H8    | [UNDO] [CLEAR] [READY / END PLANNING] |
+------------------------------------------------------------------+
| FOG OF WAR: ACTIVE             [CAMERA CONTROLS]      [ESC: MENU] |
+------------------------------------------------------------------+
```

HUD menampilkan informasi utama pertandingan, seperti giliran, fase permainan, jumlah koin, dan batas waktu perencanaan jika digunakan. Panel informasi unit menampilkan atribut unit yang sedang dipilih, sedangkan battlefield menampilkan grid, terrain, unit yang diketahui, serta penanda perintah yang telah direncanakan.

Panel perintah digunakan untuk melihat daftar aksi yang sudah diberikan kepada unit. Tombol Ready atau End Planning digunakan untuk menyelesaikan perencanaan pihak pemain. Pada pertandingan melawan AI, fase perencanaan baru berakhir ketika pemain dan AI telah siap atau batas waktu tercapai. Status kesiapan AI ditampilkan tanpa memperlihatkan perintah tersembunyinya.

Ketika War Phase dimulai, antarmuka menampilkan status eksekusi perintah, animasi gerakan, efek serangan, kerusakan, dan perubahan informasi Fog of War. Kontrol untuk memberikan perintah baru dinonaktifkan selama fase ini agar pemain memahami bahwa perintah sedang dijalankan.

### B. Panel Perintah Unit

Panel ini digunakan untuk mengatur satu perintah utama bagi setiap unit pada Planning Phase.

```text
+--------------------------------+
| UNIT: TANK                     |
| HP: 180/200                    |
| MOVE RANGE: 3                  |
| ATTACK RANGE: 15               |
|                                |
| PILIH AKSI                     |
| [MOVE]       [ATTACK]           |
|                                |
| TUJUAN / KOORDINAT              |
| X: [ 12 ]   Y: [ 08 ]           |
|                                |
| [CONFIRM COMMAND]              |
| [CANCEL]                       |
+--------------------------------+
```

Panel akan menyesuaikan pilihan berdasarkan jenis unit dan aksi yang tersedia. Untuk serangan, pemain memasukkan koordinat target secara manual. Sistem memvalidasi koordinat dan jangkauan serangan sebelum perintah disimpan. Koordinat X dan Y harus diberi label secara jelas agar tidak tertukar. Jika menggunakan notasi huruf dan angka, sistem perlu mendukung kolom di atas Z apabila ukuran grid membutuhkannya.

### C. Menu Navigasi

**Main Menu:**

- Start Game: Memulai pertandingan baru.
- How to Play: Menampilkan cara bermain, kontrol, aturan Planning Phase dan War Phase, serta mekanik Fog of War.
- Settings: Mengatur volume audio, resolusi, dan preferensi tampilan yang didukung.
- Credits: Menampilkan informasi pengembang dan sumber aset.
- Quit: Keluar dari permainan.

**Pause Menu:**

- Resume: Melanjutkan permainan.
- Restart Battle: Memulai ulang pertandingan saat ini.
- Settings: Mengubah pengaturan yang diperbolehkan selama permainan.
- Return to Main Menu: Kembali ke menu utama setelah konfirmasi.

**Victory Screen:**

- Menampilkan pesan kemenangan.
- Menampilkan jumlah giliran, unit yang tersisa, dan statistik pertempuran.
- Menampilkan total koin atau reward yang diperoleh.
- Menyediakan tombol Rematch dan Main Menu.

**Defeat Screen:**

- Menampilkan pesan kekalahan.
- Menampilkan statistik akhir pertandingan.
- Menyediakan tombol Retry dan Main Menu.

**War Phase Interface:**

- Menampilkan indikator bahwa perintah sedang dieksekusi.
- Menampilkan urutan atau status resolusi aksi.
- Memberikan feedback visual ketika unit bergerak, menyerang, menerima kerusakan, atau hancur.
- Memperbarui informasi medan perang sesuai hasil pertempuran dan aturan Fog of War.

## 3. Rencana Kebutuhan Aset (Asset Inventory)

### A. Sprite & Visual

- [ ] Sprite atau ikon unit Pistol.
- [ ] Sprite atau ikon unit Machine Gun.
- [ ] Sprite atau ikon unit Sniper.
- [ ] Sprite atau ikon unit Tank.
- [ ] Sprite atau ikon unit Mortar.
- [ ] Sprite atau ikon unit Artillery.
- [ ] Penanda kepemilikan unit pemain dan musuh.
- [ ] Tile grid dan garis koordinat.
- [ ] Tileset terrain, seperti tanah, rumput, air, dan area berbatu.
- [ ] Visual Fog of War untuk area tersembunyi dan area yang pernah terungkap.
- [ ] Indikator tile terpilih.
- [ ] Indikator jangkauan gerak.
- [ ] Indikator jangkauan serangan.
- [ ] Penanda koordinat target dan area dampak serangan.
- [ ] Efek visual gerakan, tembakan, ledakan, dan kerusakan.
- [ ] Ikon HP, damage, range, koin, dan status unit.
- [ ] Ikon perintah Move, Attack, Scan, dan Upgrade.
- [ ] Elemen UI untuk Main Menu, Pause Menu, Victory Screen, dan Defeat Screen.

### B. Audio & Musik (SFX / BGM)

- [ ] BGM Main Menu dengan suasana strategis dan atmosferik.
- [ ] BGM Planning Phase dengan tempo tenang agar pemain dapat berkonsentrasi.
- [ ] BGM War Phase dengan intensitas lebih tinggi untuk menegaskan berlangsungnya pertempuran.
- [ ] SFX pemilihan unit.
- [ ] SFX konfirmasi atau pembatalan perintah.
- [ ] SFX pergerakan unit.
- [ ] SFX tembakan dan serangan artileri.
- [ ] SFX ledakan dan dampak serangan.
- [ ] SFX unit menerima kerusakan atau hancur.
- [ ] SFX pengungkapan area Fog of War.
- [ ] SFX perolehan koin dan upgrade.
- [ ] SFX kemenangan dan kekalahan.
- [ ] SFX klik tombol antarmuka.

Audio bersifat pendukung dan tidak boleh menjadi satu-satunya sumber informasi mengenai aksi atau posisi musuh, terutama ketika informasi tersebut dibatasi oleh Fog of War.

## 4. Prinsip UX Tambahan

**Konsistensi Fase:** Planning Phase dan War Phase harus memiliki indikator visual yang jelas. Pemain perlu mengetahui kapan perintah masih dapat diubah dan kapan perintah sudah dieksekusi.

**Feedback Perintah:** Setiap perintah yang berhasil disimpan harus memiliki indikator yang terlihat. Jika perintah tidak valid, antarmuka menampilkan alasan, seperti koordinat di luar grid, target di luar jangkauan, atau tile tujuan tidak dapat ditempati.

**Keterbacaan Grid:** Koordinat harus tetap konsisten meskipun kamera digeser. Pemain dapat mengetahui koordinat tile melalui label, tooltip, atau panel informasi ketika tile dipilih.

**Informasi Terbatas:** Antarmuka tidak boleh memperlihatkan posisi unit musuh yang belum diketahui. Penanda posisi terakhir, jika ada, harus dibedakan dari posisi musuh yang sedang terlihat.

**Efisiensi Perencanaan:** Daftar perintah harus memudahkan pemain memeriksa aksi seluruh unit sebelum mengakhiri Planning Phase. Perintah dapat dibatalkan atau diubah selama fase perencanaan belum ditutup.

**Aksesibilitas:** Informasi penting menggunakan teks dan ikon selain warna. Ukuran teks, kontras, dan ukuran tombol harus tetap nyaman dibaca pada resolusi permainan yang ditargetkan.

## 5. Prioritas Implementasi UI/UX

**Prioritas 1 — UI Fungsional:**

- [ ] Tampilan grid dan koordinat.
- [ ] Pemilihan unit dan panel informasi unit.
- [ ] Tombol Move dan Attack.
- [ ] Input koordinat target.
- [ ] Daftar perintah yang telah direncanakan.
- [ ] Tombol Ready / End Planning.
- [ ] Indikator Planning Phase dan War Phase.

**Prioritas 2 — Informasi Pertempuran:**

- [ ] Indikator HP dan status unit.
- [ ] Penanda jangkauan gerak dan serangan.
- [ ] Tampilan Fog of War.
- [ ] Feedback serangan, kerusakan, dan pengungkapan area.
- [ ] Tampilan koin dan menu upgrade.

**Prioritas 3 — Penyempurnaan:**

- [ ] Main Menu, Pause Menu, Victory Screen, dan Defeat Screen.
- [ ] Pengaturan audio dan tampilan.
- [ ] Animasi transisi antarfase.
- [ ] Efek suara dan musik.
- [ ] Penyempurnaan ikon, tipografi, dan animasi UI.