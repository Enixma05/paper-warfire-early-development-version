# Spesifikasi Menu Utama, Jeda & Navigasi (menu.md)

Dokumen ini mendefinisikan struktur navigasi, alur layar antarmuka pengguna (*UI Flow*), menu utama (*Main Menu*), layar jeda (*Pause Modal*), dan layar panduan cara bermain (*How to Play*) pada **Paper Warfire** (Tanggung Jawab Role 3).

---

## 1. Diagram Alur Navigasi Antarmuka (UI Navigation Flow)

```text
                        +----------------------+
                        |      MAIN MENU       |
                        +----------+-----------+
                                   |
         +-----------------+-------+-------+-----------------+
         |                 |               |                 |
         v                 v               v                 v
  [START BATTLE]     [HOW TO PLAY]    [SETTINGS]          [QUIT]
         |                 |               |                 |
         v                 +-------+-------+                 v
  +--------------+                 |                    [Keluar Game]
  |  BATTLEFIELD | <---------------+ (Kembali ke Menu)
  |  (GAMEPLAY)  |
  +-------+------+
          |
     [Tekan ESC]
          |
          v
  +--------------+
  | PAUSE MODAL  | ──► [RESUME / RESTART / SETTINGS / QUIT TO MENU]
  +--------------+
```

---

## 2. Layar Menu Utama (Main Menu Screen)

- **Latar Belakang Visual:** Grid kertas militer bernuansa abu-abu gelap kebiruan (`#252830`) dengan siluet geometris tank dan garis koordinat taktis yang bergerak perlahan di latar belakang (*subtle pan animation*).
- **Tipografi Judul:** Teks **"PAPER WARFIRE"** berukuran besar di tengah atas dengan efek bayangan tajam (*clean drop shadow*).
- **Sub-judul:** *"Simultaneous Turn-Based Grid Strategy"*.
- **Tombol Navigasi Utama:**
  1. **MULAI PERTEMPURAN (Start Battle):** Menginisialisasi grid medan perang baru secara prosedural dan masuk ke `Planning Phase`.
  2. **CARA BERMAIN (How to Play):** Membuka panel edukasi aturan WEGO dan Fog of War.
  3. **PENGATURAN (Settings):** Mengatur slider volume Master, BGM, dan SFX.
  4. **KREDIT (Credits):** Menampilkan nama 3 anggota tim pengembang dan pembagian peran.
  5. **KELUAR (Quit):** Menutup aplikasi secara aman (`pygame.quit()`, `sys.exit()`).

---

## 3. Modal Layar Jeda (Pause Screen Modal)

Sesuai prinsip **Pencegahan Frustrasi (Rubrik UX poin 5)**, pemain dapat menjeda permainan kapan saja saat `Planning Phase` tanpa kehilangan progres perintah:

- **Aktivasi:** Menekan tombol `Escape` atau tombol `P` pada keyboard, atau mengklik ikon gerigi di pojok layar.
- **Tampilan Visual:** Overlay semi-transparan hitam (`rgba(0, 0, 0, 180)`) menggelapkan arena pertempuran di latar belakang.
- **Daftar Opsi Tombol:**
  1. **Lanjutkan (Resume):** Menutup modal dan kembali ke perencanaan unit.
  2. **Ulangi Pertandingan (Restart Match):** Memunculkan dialog konfirmasi ("Apakah Anda yakin ingin memulai ulang medan perang?"). Jika Ya, reset seed peta dan unit.
  3. **Pengaturan Suara (Audio Options):** Slider cepat untuk mengatur volume audio saat bermain.
  4. **Kembali ke Menu Utama (Main Menu):** Kembali ke menu awal setelah konfirmasi.

---

## 4. Modal Panduan Cara Bermain (How to Play Overlay)

Untuk memenuhi **Kejelasan Tujuan (Rubrik UX poin 1)** agar pemain awam memahami permainan dalam 1 menit pertama:

Layar panduan dibagi menjadi 3 tab ringkas yang mudah dipahami:
1. **Tab 1: Mekanik Dua Fase (WEGO):**
   - Penjelasan bahwa perintah disusun bersamaan di `Planning Phase`, lalu dieksekusi serentak di `War Phase`.
2. **Tab 2: Menembak di Balik Kabut (Fog of War & Coordinates):**
   - Penjelasan bahwa musuh tidak terlihat jika di balik kabut, dan pemain dapat menebak koordinat sasaran tembak atau memakai area ledakan 3x3 untuk membuka kabut.
3. **Tab 3: Peran Pasukan & Kondisi Menang:**
   - Ringkasan fungsi Infanteri, Sniper, Tank, dan Artileri.
   - Penegasan objektif: *"Hancurkan seluruh unit lawan untuk memenangkan perang!"*.

---

## 5. Sistem Umpan Balik Tombol & Transisi (Audio-Visual Feel)

- **Hover Effect:** Tombol membesar sebesar $105\%$ dengan garis tepi kuning keemasan (`#F2C14E`) saat kursor mouse berada di atas tombol.
- **Active Click Effect:** Tombol bergeser 2 piksel ke bawah (*pressed depth*) dan memutar SFX klik taktil.
- **Transisi Antar Layar:** Efek fade-in / fade-out hitam lembut selama 0.2 detik untuk menghindari perpindahan visual yang kasar.
