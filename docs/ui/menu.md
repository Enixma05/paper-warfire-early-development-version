# Spesifikasi Menu Utama & Pause (menu.md)

Dokumen ini mendefinisikan rancangan antarmuka Menu Utama (*Title Screen*), Menu Jeda (*Tactical Pause Screen*), modal petunjuk bermain (*How to Play*), dan alur navigasi tombol (Tanggung Jawab: **Role 3 — UI/UX Designer, Audio/Asset Integrator & QA**).

---

## 1. Antarmuka Menu Utama (Main Menu - `MENU_STATE`)

Layar pertama yang menyambut pemain saat game dibuka. Mengusung tema estetika *Retro Cyber-Cold War Military Terminal*.

```
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|                                                                                                   |
|                                  OPERATION: PHANTOM WIRE                                          |
|                                [TACTICAL STEALTH ESPIONAGE]                                       |
|                                                                                                   |
|                                                                                                   |
|                                    [ 1. MULAI MISI ]                                              |
|                                    [ 2. CARA BERMAIN ]                                            |
|                                    [ 3. KREDIT TIM ]                                              |
|                                    [ 4. KELUAR ]                                                  |
|                                                                                                   |
|                                                                                                   |
|                                                                                                   |
| [v1.0 - UTS FINAL PROJECT]                                              [NAVIGASI: PANAH / ENTER] |
+---------------------------------------------------------------------------------------------------+
```

### A. Rincian Elemen & Interaksi:
- **Judul Game:** Tipografi tebal dengan efek pendaran hijau/cyan fosfor (*Scanline Terminal Glow*).
- **Daftar Opsi Tombol:**
  1. `MULAI MISI`: Menginisialisasi `PLAY_STATE` dan memuat peta Sektor A.
  2. `CARA BERMAIN`: Membuka modal overlay petunjuk kontrol dan objektif kemenangan.
  3. `KREDIT TIM`: Menampilkan pop-up nama anggota kelompok dan peran masing-masing.
  4. `KELUAR`: Menutup aplikasi secara bersih (`pygame.quit()`, `sys.exit()`).
- **Respon Interaksi (Feedback):**
  - Tombol yang sedang dipilih (*hovered/focused*) membesar 8%, berubah warna menjadi kuning cerah, dan memutar SFX ketukan terminal singkat.

---

## 2. Modal Petunjuk Bermain (How to Play Overlay)

Dapat diakses dari menu utama untuk memastikan pemain memahami aturan permainan sebelum memulai (sesuai **Rubrik UX - Kejelasan Tujuan**):

- **Tampilan Kontrol:**
  - `W, A, S, D` : Bergerak senyap di balik bayangan.
  - `Left Shift` : Lari cepat (*Sprint*) — *Perhatian: Suara langkah terdengar musuh!*
  - `Space / E`  : Ketuk dinding untuk memancing penjaga / Takedown musuh dari belakang / Sabotase generator.
  - `Klik Kiri / J` : Tembak pistol penenang (*Tranq Dart*) — *Amunisi hanya 3!*
  - `Escape / P` : Buka menu jeda taktis.
- **Tips Taktis Utama:** *"Hindari garis kerucut pandang musuh. Jika alarm berbunyi, segera cari tempat sembunyi di locker atau lorong gelap hingga hitungan mundur selesai."*

---

## 3. Menu Jeda Taktis (Pause Screen - `PAUSE_STATE`)

Diaktifkan saat pemain menekan tombol `Escape` atau `P` di tengah permainan:

```
+---------------------------------------------------------------------------------------------------+
| ############################## [ LAYAR PERMAINAN DIBEKUKAN ] #################################### |
| ################################################################################################# |
|                                                                                                   |
|                                   === TACTICAL PAUSE ===                                          |
|                                                                                                   |
|                                    [ LANJUTKAN MISI ]                                             |
|                                    [ RESTART LEVEL ]                                              |
|                                    [ MENU UTAMA ]                                                 |
|                                                                                                   |
|                                                                                                   |
| ################################################################################################# |
| ################################################################################################# |
+---------------------------------------------------------------------------------------------------+
```

### Logika & Aturan Eksekusi:
1. **Pembekuan Waktu (Time Freeze):**
   - Siklus `update` pada seluruh pergerakan musuh, kalkulasi peluru, dan hitungan mundur alarm dihentikan sementara.
2. **Visual Overlay:**
   - Tangkapan layar frame terakhir dilapisi surface hitam semi-transparan (alpha = 180) dengan efek vignette halus.
3. **Pencegahan Frustrasi (Error Prevention):**
   - Pemain memiliki kebebasan penuh untuk memulai ulang level secara instan (*Quick Restart*) jika melakukan kesalahan infiltrasi tanpa harus menutup paksa aplikasi.
   - Pilihan `MENU UTAMA` meminta konfirmasi singkat sebelum keluar.
