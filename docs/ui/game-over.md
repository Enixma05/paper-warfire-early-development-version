# Spesifikasi Layar Akhir Pertandingan (game-over.md)

Dokumen ini mendefinisikan rancangan antarmuka Layar Kemenangan (*Victory Screen*), Layar Kekalahan (*Defeat Screen*), rekap statistik pertempuran, serta alur pengulangan permainan pada **Paper Warfire** (Tanggung Jawab Role 3).

---

## 1. Layar Kemenangan (Victory Screen)

Layar ini ditampilkan ketika seluruh unit lawan berhasil dieliminasi oleh pasukan pemain:

```text
+--------------------------------------------------------------------------+
|                                                                          |
|                         ★ KEMENANGAN TELAK! ★                            |
|                       (MISSION ACCOMPLISHED)                             |
|                                                                          |
|                  Seluruh Kekuatan Lawan Telah Dihancurkan                |
|                                                                          |
|    +----------------------------------------------------------------+    |
|    |                      LAPORAN PERTEMPURAN                       |    |
|    | - Jumlah Giliran Diperlukan : 08 Giliran                       |    |
|    | - Unit Kawan yang Bertahan  : 4 / 6 Unit                       |    |
|    | - Total Unit Lawan Musnah   : 6 / 6 Unit                       |    |
|    | - Area Medan Terungkap (FoW): 78%                              |    |
|    | - Total Koin Diperoleh      : 520 Koin                         |    |
|    | - Akurasi Tembakan Taktis   : 64%                              |    |
|    +----------------------------------------------------------------+    |
|                                                                          |
|                 [ MAIN LAGI (REMATCH) ]      [ MENU UTAMA ]              |
|                                                                          |
+--------------------------------------------------------------------------+
```

### Karakteristik Visual & Audio Kemenangan:
- **Warna Tema:** Hijau kemenangan (`#536B4F`) berpadu dengan aksen emas militer (`#F2C14E`).
- **Efek Visual:** Partikel bintang geometris berpendar di latar belakang dan banner animasi meluncur turun secara elegan.
- **Audio Feedback:** Memutar lagu kemenangan (*Victory Fanfare*) bernada heroik dan gagah.

---

## 2. Layar Kekalahan (Defeat / Game Over Screen)

Layar ini ditampilkan ketika seluruh unit pemain musnah atau batas giliran maksimal pertandingan terlampaui:

```text
+--------------------------------------------------------------------------+
|                                                                          |
|                         ✖ PASUKAN ANDA KALAH ✖                          |
|                            (BATTLE LOST)                                 |
|                                                                          |
|              Pertahanan Markas Tembus dan Pasukan Telah Gugur            |
|                                                                          |
|    +----------------------------------------------------------------+    |
|    |                      EVALUASI PERTEMPURAN                      |    |
|    | - Bertahan Hingga Giliran   : Giliran 12                       |    |
|    | - Sisa Pasukan Kawan        : 0 Unit                           |    |
|    | - Unit Musuh Berhasil Dihabisi: 3 Unit                         |    |
|    | - Total Koin Terkumpul      : 210 Koin                         |    |
|    | - Catatan Strategi: Amankan garis depan dengan Tank dan intai  |    |
|    |   posisi artileri musuh lebih awal menggunakan infanteri!      |    |
|    +----------------------------------------------------------------+    |
|                                                                          |
|               [ COBA LAGI (RETRY) ]       [ KEMBALI KE MENU ]            |
|                                                                          |
+--------------------------------------------------------------------------+
```

### Karakteristik Visual & Audio Kekalahan:
- **Warna Tema:** Latar belakang menggelap dengan aksen merah peringatan tebal (`#E05252`).
- **Efek Visual:** Vignette merah redup di sudut-sudut layar dengan teks tebal bergetar singkat (*shake impact*).
- **Audio Feedback:** SFX nada kekalahan muram bernuansa drum militer lambat.
- **Nilai Edukasi (UX Anti-Frustrasi):** Menampilkan tips strategi singkat agar pemain terdorong mencoba taktik baru di percobaan berikutnya.

---

## 3. Opsi Navigasi & Siklus Restart

Kedua layar akhir menyediakan dua tombol navigasi utama:
1. **Coba Lagi / Main Lagi (Retry / Rematch):**
   - Menginisialisasi ulang battlefield dengan peta baru secara instan tanpa perlu memuat ulang seluruh aplikasi.
   - Mengembalikan pemain ke `Planning Phase` giliran 1.
2. **Kembali ke Menu Utama (Main Menu):**
   - Menyimpan statistik sesi lokal jika ada, lalu melakukan transisi kembali ke `MENU_STATE`.
