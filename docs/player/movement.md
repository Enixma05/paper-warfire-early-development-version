# Spesifikasi Pergerakan Pasukan Pemain (movement.md)

Dokumen ini mendefinisikan sistem navigasi berbasis grid (*Grid-Based Navigation*), aturan jangkauan gerak (*Movement Range*), validasi tile tujuan, penanganan tabrakan, dan visualisasi lintasan pergerakan unit pemain pada **Paper Warfire** (Tanggung Jawab Role 2).

---

## 1. Aturan Pergerakan Grid (Grid-Based Movement Mechanics)

Pergerakan dalam Paper Warfire tidak menggunakan kontrol analog atau real-time physics, melainkan **perencanaan perpindahan diskrit antar tile** pada medan perang berukuran $24 \times 16$ tile:

1. **Satu Perintah Gerak per Giliran:**
   - Selama **Planning Phase**, pemain dapat memilih satu unit miliknya dan menetapkan satu koordinat tile tujuan (`target_x, target_y`).
   - Perintah disimpan ke dalam antrean perintah pemain (`player_commands`) dan **belum dieksekusi** hingga War Phase dimulai.
2. **Jangkauan Gerak Maksimal (Movement Range / `move_range`):**
   - Jarak tempuh dihitung menggunakan metrik jarak grid Manhattan (atau jarak orthogonal 4-arah / diagonal 8-arah yang diizinkan):
     $$\text{Distance}(\text{Start}, \text{Target}) \le \text{unit.move\_range}$$
   - Setiap jenis unit memiliki batas langkah per giliran:
     - **Pistol Unit:** 4 tile (mobilitas tinggi, infanteri ringan).
     - **Machine Gun:** 3 tile (mobilitas sedang).
     - **Tank Unit:** 3 tile (kendaraan lapis baja berat).
     - **Sniper Unit:** 2 tile (mobilitas rendah, penembak statis).
     - **Mortar Unit:** 2 tile (tim artileri jinjing).
     - **Artillery Unit:** 1 tile (kendaraan artileri berat statis).

---

## 2. Pengaruh Terrain terhadap Biaya Gerak (Movement Cost & Pathfinding)

Setiap tile memiliki nilai biaya langkah (*movement cost*). Total akumulasi biaya langkah tidak boleh melebihi `move_range` unit:

| Tipe Medan (Terrain) | Biaya Langkah (Movement Cost) | Status Aksesibilitas |
| :--- | :--- | :--- |
| **Plains / Rumput** | $1.0$ poin gerak | Dapat dilalui semua unit |
| **Forest / Hutan** | $2.0$ poin gerak | Memperlambat unit; kendaraan berat (Tank) butuh usaha ekstra |
| **Swamp / Rawa** | $2.0$ poin gerak | Memperlambat laju pasukan |
| **Mountain / Batu** | $\infty$ (Impassable) | **Tidak dapat dilalui** oleh unit darat apa pun |
| **Tile Berpenghuni** | $\infty$ (Blocked) | Tidak boleh berhenti di tile yang sudah ditempati unit kawan |

---

## 3. Resolusi Tabrakan Pergerakan Simultan (WEGO Collision Resolution)

Karena kedua pihak bergerak secara serentak pada **War Phase**, aturan tabrakan pergerakan didefinisikan secara deterministik:

```text
Kasus A: Dua unit (Kawan & Lawan) menuju tile kosong yang SAMA pada giliran yang sama.
Resolusi:
1. "Head-on Collision / Bouncing":
   - Kedua unit membatalkan pergerakannya dan tetap berada di tile asal mereka.
   - Kedua unit menerima 10 contact damage akibat benturan.
   - Tile tujuan memunculkan efek visual benturan (clash particle).

Kasus B: Unit Pemain mencoba bergerak ke tile yang ditempati musuh yang diam (tidak bergerak).
Resolusi:
1. Sistem validasi antarmuka pada Planning Phase melarang pemilihan tile yang terlihat jelas dihuni musuh.
2. Jika musuh tersembunyi di Fog of War dan tidak sengaja ditabrak:
   - Unit pemain berhenti 1 tile sebelum tile musuh (terinterupsi / ambush).
   - Musuh langsung terungkap dari kabut perang.
```

---

## 4. Visualisasi & Indikator UI Pergerakan (Player Feedback)

Pada saat pemain memilih unit di Planning Phase:
1. **Highlight Movement Radius (Area Kuning/Biru Redup):**
   - Sistem melakukan flood-fill algoritma BFS (*Breadth-First Search*) untuk mewarnai seluruh tile yang sah dijangkau oleh unit tersebut.
2. **Garis Lintasan (Path Arrow Indicator):**
   - Saat kursor mouse diarahkan ke tile tujuan yang valid, muncul garis putus-putus (*dashed line trajectory*) dari posisi unit ke tile target.
3. **Ghost Marker:**
   - Siluet transparan unit (*ghost sprite*) diletakkan pada tile tujuan untuk memberi kepastian visual kepada pemain tentang posisi akhir unit setelah War Phase.
