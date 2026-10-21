# Sketsa Mekanik & Aturan Bermain (Mechanics Sketch)

## 1. Skema Kontrol (Player Controls)

| Input / Tombol | Aksi Pemain | Keterangan / Feedback |
|---|---|---|
| Mouse Left Click | Memilih unit atau tile | Menampilkan informasi unit, koordinat tile, dan status medan perang. |
| Mouse Left Click pada UI | Memilih aksi unit | Membuka opsi bergerak, menyerang, atau menggunakan kemampuan khusus. |
| Keyboard / Input Koordinat | Menentukan koordinat target serangan | Pemain memasukkan koordinat tile target, kemudian sistem memvalidasi format dan jangkauan senjata. |
| Tombol Move | Menetapkan perintah bergerak | Menyimpan tujuan pergerakan unit untuk dieksekusi pada War Phase. |
| Tombol Attack | Menetapkan perintah menyerang | Menyimpan jenis serangan dan koordinat target tanpa langsung menimbulkan kerusakan. |
| Tombol Recon / Scan | Menentukan area pengintaian | Mengungkap area tertentu sesuai jangkauan kemampuan dan aturan permainan. |
| Tombol Confirm Command | Mengonfirmasi perintah unit | Menandai perintah sebagai siap dieksekusi. |
| Tombol Execute / End Planning | Mengakhiri fase perencanaan | Memulai War Phase setelah kedua pihak siap atau batas waktu perencanaan berakhir. |
| Tombol Upgrade | Meningkatkan kemampuan unit | Menggunakan koin untuk membeli peningkatan yang tersedia. |
| Mouse Scroll / WASD | Menggeser kamera | Menggerakkan tampilan medan perang tanpa mengubah koordinat tile atau posisi unit. |
| Escape / P | Membuka menu jeda | Menampilkan menu jeda dan opsi melanjutkan atau keluar dari pertandingan, sesuai aturan mode permainan. |

Catatan: Jika game hanya memiliki satu pemain manusia melawan AI, perencanaan kedua pihak tetap dapat berlangsung secara bersamaan dari sudut pandang sistem. Pemain mengatur unit melalui antarmuka, sedangkan AI menyusun perintahnya di latar belakang. Jika mendukung dua pemain manusia, diperlukan mekanisme untuk menyembunyikan perintah lawan selama Planning Phase.

## 2. Aksi & Kemampuan Utama (Core Mechanics)

**Sistem Gerak:**

Paper Warfire menggunakan sistem pergerakan berbasis grid. Setiap unit menempati satu atau beberapa tile, bergantung pada ukuran dan jenisnya. Pemain menentukan tile tujuan selama Planning Phase, kemudian pergerakan dijalankan pada War Phase. Pergerakan dibatasi oleh jangkauan gerak unit, kondisi terrain, keberadaan unit lain, dan aturan tabrakan yang ditetapkan. Kamera dapat digeser untuk melihat bagian medan perang yang lebih luas tanpa mengubah koordinat tile.

**Sistem Tempur (Combat/Interaksi):**

Sistem tempur menggunakan mekanik Command Planning. Pemain dan lawan menyusun perintah secara bersamaan, tetapi tidak ada serangan atau pergerakan yang langsung dieksekusi selama fase perencanaan. Setelah kedua pihak selesai merencanakan, perintah diproses pada War Phase.

Setiap unit hanya dapat menerima satu perintah utama per giliran, yaitu bergerak atau menyerang. Serangan ditentukan melalui koordinat target yang dimasukkan pemain. Sistem memeriksa validitas koordinat, jangkauan senjata, kondisi target, kerusakan, dan area dampak. Untuk senjata dengan area serangan, tile di sekitar titik target dapat ikut terdampak sesuai karakteristik senjata. Jika unit berpindah atau target berubah sebelum serangan diselesaikan, hasilnya mengikuti aturan resolusi yang telah ditentukan.

**Sistem Fog of War:**

Fog of War membatasi informasi yang dapat diketahui pemain mengenai medan perang. Tile dibedakan menjadi area yang belum diketahui, area yang pernah terungkap, dan area yang sedang terlihat. Posisi unit musuh tidak otomatis diketahui ketika berada di luar pengamatan. Serangan yang mengenai atau jatuh pada suatu area dapat mengungkap tile di sekitar titik dampak. Kemampuan pengintaian juga dapat digunakan untuk memperoleh informasi tanpa harus melancarkan serangan secara langsung.

**Sistem AI Musuh:**

AI musuh menggunakan pendekatan berbasis aturan (*rule-based AI*). AI menyusun perintah berdasarkan posisi musuh yang terlihat, informasi terakhir yang diketahui, karakteristik unit, dan kondisi medan perang. Jika tidak mengetahui posisi pemain, AI dapat bergerak menuju area strategis atau mencari lokasi yang diperkirakan menjadi tempat keberadaan pemain. AI tidak diperbolehkan mengakses posisi pemain yang seharusnya tersembunyi oleh Fog of War.

**Resource Pemain:**

- Health: Setiap unit memiliki HP sesuai jenis dan perannya. Unit dianggap hancur ketika HP mencapai 0.
- Damage: Besarnya kerusakan yang diberikan bergantung pada jenis senjata dan aturan pertempuran.
- Movement Range: Jarak maksimum yang dapat ditempuh unit dalam satu perintah bergerak.
- Attack Range: Jarak maksimum serangan yang dapat dilakukan unit.
- Coins: Sumber daya yang diperoleh berdasarkan hasil pertempuran dan dapat digunakan untuk meningkatkan kemampuan unit.
- Command Limit: Setiap unit hanya dapat menerima satu perintah utama per giliran.
- Planning Timer: Batas waktu untuk menyusun perintah, jika mekanik batas waktu diterapkan. Durasi final ditentukan pada tahap penyeimbangan permainan.

## 3. Jenis Unit dan Peran Taktis (Unit Archetypes)

**1. Pistol Unit (Unit Dasar)**

- Perilaku: Unit infanteri dasar yang dapat bergerak dan menyerang target dalam jangkauan pendek.
- Peran: Unit serbaguna untuk pertempuran jarak dekat hingga menengah.
- Jangkauan Serangan: 6 tile.
- Damage: Rendah.
- Area Serangan: Terbatas pada satu tile target.
- Ukuran: 1 × 1 tile.

**2. Machine Gun Unit (Unit Area Suppression)**

- Perilaku: Menyerang area untuk memberikan tekanan terhadap beberapa unit atau lokasi.
- Peran: Mengendalikan area dan mengganggu konsentrasi pasukan lawan.
- Jangkauan Serangan: 8 tile.
- Damage: Rendah.
- Area Serangan: Area 3 × 3 tile, dengan tile pusat sebagai sasaran utama dan kemungkinan dampak pada tile sekitar sesuai aturan senjata.
- Ukuran: 1 × 1 tile, kecuali ukuran khusus ditetapkan pada tahap pengembangan.

**3. Sniper Unit (Unit Jarak Jauh)**

- Perilaku: Menyerang satu target dari jarak jauh dengan kerusakan tinggi.
- Peran: Mengeliminasi unit prioritas dan mendukung pasukan dari jarak jauh.
- Jangkauan Serangan: 12 tile.
- Damage: Tinggi.
- Area Serangan: Satu tile target.
- Ukuran: 1 × 1 tile.

**4. Tank Unit (Unit Berat)**

- Perilaku: Bergerak dan menyerang menggunakan daya tahan serta daya rusak yang tinggi.
- Peran: Menjadi unit garis depan dan menekan posisi lawan.
- Jangkauan Serangan: 15 tile.
- Damage: Tinggi.
- Area Serangan: Dapat menggunakan area dampak 3 × 3 tile jika ditetapkan sebagai karakteristik senjatanya.
- Ukuran: 2 × 3 tile.

**5. Mortar Unit (Unit Artileri Menengah)**

- Perilaku: Menyerang lokasi dari jarak menengah hingga jauh menggunakan serangan area.
- Peran: Memberikan dukungan tembakan terhadap area yang diperkirakan ditempati musuh.
- Jangkauan Serangan: 18 tile.
- Damage: Menengah.
- Area Serangan: 3 × 3 tile.
- Ukuran: Ditentukan berdasarkan rancangan footprint unit.

**6. Artillery Unit (Unit Artileri Berat)**

- Perilaku: Melakukan serangan jarak jauh dengan kerusakan tinggi terhadap koordinat target.
- Peran: Menekan posisi pertahanan dan area yang diduga menjadi konsentrasi musuh.
- Jangkauan Serangan: 25 tile.
- Damage: Tinggi.
- Area Serangan: 3 × 3 tile.
- Ukuran: Dapat menggunakan footprint lebih besar sesuai rancangan.

**7. Grenade Unit / Grenade Attack**

- Perilaku: Melakukan serangan area pada jarak pendek.
- Peran: Menyerang unit atau kelompok musuh yang berada berdekatan.
- Jangkauan Serangan: 5 tile.
- Damage: Tinggi.
- Area Serangan: 3 × 3 tile.
- Catatan: Perlu ditentukan apakah granat menjadi kemampuan unit tertentu atau jenis serangan yang dapat digunakan oleh unit khusus.

Catatan: Nilai damage numerik, HP, biaya perekrutan, biaya upgrade, serta aturan jangkauan final belum ditetapkan. Nilai tersebut perlu disesuaikan melalui pengujian keseimbangan permainan. Jenis unit tambahan seperti kapal, serangan udara, RPG, dan peluncur misil dapat dimasukkan sebagai pengembangan lanjutan setelah mekanik inti berjalan stabil.

## 4. Syarat Menang & Kalah (Win / Lose Conditions)

**Syarat Menang (Victory):**

- Menghancurkan seluruh unit utama lawan atau memenuhi kondisi eliminasi yang ditentukan untuk pertandingan.
- Jika permainan menggunakan objektif khusus, kemenangan dapat dicapai dengan menguasai lokasi strategis atau menyelesaikan objektif tertentu.
- Kondisi kemenangan diperiksa setelah seluruh perintah pada War Phase selesai diproses dan hasil pertempuran diperbarui.

**Syarat Kalah (Defeat):**

- Seluruh unit utama milik pemain hancur atau kondisi kekalahan yang ditetapkan telah terpenuhi.
- Pemain gagal mempertahankan objektif utama, apabila mode permainan menggunakan objektif.
- Jika batas waktu pertandingan diterapkan, pemain kalah apabila waktu berakhir sebelum kondisi kemenangan terpenuhi.

**Aturan Penyelesaian Giliran:**

- Planning Phase berakhir ketika kedua pihak menyatakan siap atau batas waktu perencanaan tercapai.
- War Phase memproses perintah yang telah disimpan sesuai aturan resolusi permainan.
- Unit yang hancur tidak dapat menjalankan perintah berikutnya. Jika unit hancur sebelum perintahnya diproses, sistem menggunakan aturan resolusi yang telah ditentukan untuk membatalkan atau menangani perintah tersebut.
- Setelah resolusi selesai, sistem memeriksa kondisi kemenangan dan kekalahan.
- Jika pertandingan belum berakhir, pemain memperoleh koin sesuai aturan reward, dapat melakukan upgrade, lalu memasuki giliran berikutnya.

## 5. Item & Power-ups (Opsional)

| Nama Item / Kemampuan | Efek | Cara Memperoleh / Penggunaan |
|---|---|---|
| Scan Location Units | Mengungkap area tertentu untuk membantu menemukan posisi musuh. | Menggunakan kemampuan pengintaian dengan biaya atau batas penggunaan yang ditentukan. |
| Air Defend | Mengurangi atau mencegah dampak serangan udara pada area tertentu. | Diaktifkan sebagai kemampuan pertahanan sesuai aturan dan durasi yang ditentukan. |
| Penetration Upgrade | Meningkatkan damage atau kemampuan menembus pertahanan target. | Dibeli menggunakan koin pada fase upgrade. |
| Scope Upgrade | Meningkatkan jangkauan serangan unit tertentu. | Dibeli menggunakan koin pada fase upgrade. |
| Magazine Upgrade | Meningkatkan jumlah tembakan atau kapasitas serangan sesuai aturan unit. | Dibeli menggunakan koin pada fase upgrade. |

Catatan: Item dan power-up bersifat opsional. Implementasi awal sebaiknya memprioritaskan Command Planning, War Phase, pergerakan unit, serangan berbasis koordinat, dan Fog of War. Sistem upgrade dan power-up dapat ditambahkan setelah mekanik inti berhasil diuji.