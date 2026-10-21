# Brainstorming & Ide Inti Game (Core Concept)

## 1. High Concept & Elevator Pitch

**Judul Game (Tentatif):** Paper Warfire

**Genre Utama:** 2D Grid-Based Turn-Based Strategy dengan mekanik WEGO(*We Go*). dan Fog Of War 

**Elevator Pitch:**

Paper Warfire adalah game strategi turn-based berbasis grid yang memungkinkan dua pihak merencanakan pergerakan dan serangan unit secara bersamaan sebelum seluruh perintah dieksekusi pada fase pertempuran. Dengan mekanik Command Planning, Fog of War, dan serangan berbasis koordinat, pemain dituntut menyusun strategi, memperkirakan posisi lawan, serta mengambil keputusan berdasarkan informasi medan perang yang terbatas.

## 2. Premis Cerita & Tema Dunia (Setting)

**Tema Visual / Suasana (Vibe):**

Medan perang bergaya minimalis yang terinspirasi dari permainan perang menggunakan kertas dan gambar sederhana. Visual permainan menggunakan representasi unit berbentuk sederhana, seperti figur tentara, tank, artileri, dan kendaraan militer lainnya di atas arena grid. Suasana permainan berfokus pada strategi, ketidakpastian, dan perencanaan taktis, bukan pada detail visual atau simulasi perang yang kompleks.

**Premis Cerita Singkat:**

Paper Warfire menggambarkan konflik antara dua kekuatan militer yang berusaha menguasai medan perang melalui perencanaan dan penggunaan sumber daya secara efektif. Setiap pihak harus mengatur unit, menentukan pergerakan, serta merencanakan serangan dengan mempertimbangkan posisi musuh yang belum sepenuhnya diketahui. Medan perang yang dihasilkan secara acak dan penerapan Fog of War membuat setiap pertempuran menghadirkan kondisi yang berbeda sehingga pemain harus menyesuaikan strategi pada setiap giliran.

## 3. Pilar Desain Game (Core Pillars)

**Pilar 1: Command Planning & Simultaneous Orders**

Pemain dan lawan merencanakan perintah unit secara bersamaan pada Planning Phase. Setiap unit memiliki batasan satu perintah utama dalam satu giliran, seperti bergerak atau menyerang. Perintah yang telah disusun tidak langsung dieksekusi, tetapi disimpan sampai War Phase dimulai. Mekanik ini mendorong pemain untuk mempertimbangkan kemungkinan tindakan lawan sebelum menentukan keputusan.

**Pilar 2: Fog of War & Information-Based Strategy**

Informasi medan perang dibatasi melalui mekanik Fog of War sehingga posisi unit lawan tidak selalu diketahui. Pemain dapat memperoleh informasi melalui pengamatan, kemampuan pengintaian, dan pengungkapan area akibat serangan. Sistem serangan berbasis koordinat menuntut pemain memanfaatkan informasi yang tersedia untuk menentukan lokasi target, sekaligus mempertimbangkan risiko ketika menyerang area yang belum diketahui secara pasti.

**Pilar 3: Tactical Positioning & Resource Management**

Posisi, jangkauan serangan, karakteristik unit, dan penggunaan sumber daya memengaruhi keputusan taktis pemain. Setiap unit memiliki atribut dan fungsi yang berbeda. Setelah pertempuran pada suatu giliran selesai, pemain dapat memperoleh koin untuk meningkatkan kemampuan pasukan atau mempersiapkan strategi berikutnya. Arena berbasis grid dan medan perang yang dihasilkan secara acak memberikan variasi kondisi pertempuran.

## 4. Inspirasi & Game Referensi

| Judul Game Referensi | Elemen yang Diadaptasi / Menarik |
|---|---|
| Frozen Synapse | Pendekatan WEGO, yaitu perencanaan perintah sebelum aksi kedua pihak dieksekusi dalam fase resolusi. |
| Advance Wars | Pertempuran berbasis grid, variasi unit, jangkauan serangan, dan pengambilan keputusan taktis. |
| Battle for Wesnoth | Pertempuran berbasis hex/grid, karakteristik unit, terrain, serta pengelolaan pasukan. |
| Age of Empires | Konsep Fog of War, pengintaian, dan keterbatasan informasi mengenai posisi lawan. |
| Into the Breach | Perencanaan aksi, penggunaan posisi pada grid, serta pertimbangan konsekuensi tindakan sebelum eksekusi. |

Game referensi tersebut digunakan sebagai sumber inspirasi mekanik dan desain. Paper Warfire tetap memiliki identitas tersendiri melalui perencanaan perintah secara bersamaan, serangan berbasis koordinat manual, pengungkapan area medan perang, serta visual minimalis yang terinspirasi dari permainan perang di atas kertas.

## 5. Core Game Loop (Sketsa Ide)

```text
[Persiapan Pertempuran]
          |
          v
[Pembangkitan Medan Perang]
          |
          v
[Penempatan dan Pemeriksaan Unit]
          |
          v
[Planning Phase]
Kedua pihak menyusun perintah
secara bersamaan
          |
          v
[War Phase]
Perintah kedua pihak dieksekusi
          |
          v
[Resolusi Pertempuran]
Pergerakan, serangan, dan kerusakan
          |
          v
[Pengungkapan Informasi]
Pembaruan Fog of War dan posisi
musuh yang diketahui
          |
          v
[Evaluasi Hasil Giliran]
          |
          v
[Perolehan Koin dan Upgrade]
          |
          v
{Kondisi Kemenangan Terpenuhi?}
       /             \
     Ya               Tidak
     |                  |
     v                  v
[Pertempuran Selesai] [Planning Phase]
                        Giliran Berikutnya
```

**Deskripsi Loop:**

Permainan dimulai dengan pembangkitan medan perang dan penempatan unit pada area awal masing-masing pihak. Ketika Planning Phase dimulai, pemain dan lawan menyusun perintah unit secara bersamaan berdasarkan informasi yang mereka miliki. Setiap perintah disimpan sampai fase perencanaan berakhir, kemudian dieksekusi pada War Phase sesuai aturan resolusi yang ditetapkan.

Setelah perintah selesai diproses, sistem menghitung hasil pertempuran, memperbarui kondisi unit, dan mengungkap informasi medan perang berdasarkan pengamatan serta dampak serangan. Pemain kemudian memperoleh koin yang dapat digunakan untuk meningkatkan kemampuan pasukan. Jika kondisi kemenangan belum terpenuhi, permainan berlanjut ke Planning Phase berikutnya. Siklus ini berlangsung sampai salah satu pihak memenuhi kondisi kemenangan atau kekalahan yang telah ditentukan.