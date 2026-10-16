# Spesifikasi Menu Utama & Pause (menu.md)

Spesifikasi antarmuka menu utama, alur navigasi tombol, dan menu jeda (Pause Screen).

---

## 1. Menu Utama (Main Menu)
- **Judul Game:** Ditampilkan di tengah atas dengan ukuran font besar dan bayangan (drop shadow).
- **Daftar Tombol Navigasi:**
  1. `MULAI PERMAINAN`: Transisi ke `PLAY_STATE`.
  2. `CARA BERMAIN`: Membuka modal overlay petunjuk kontrol dan objektif kemenangan.
  3. `KELUAR`: Menutup jendela game (`pygame.quit()`, `sys.exit()`).
- **Interaksi Tombol:**
  - Efek *hover* mouse / navigasi panah: Tombol berubah warna kontras dan memutar SFX klik lembut.

## 2. Layar Jeda (Pause Screen)
- Diaktifkan saat pemain menekan tombol `Escape` atau `P` di `PLAY_STATE`.
- **Visual:** Render overlay hitam semi-transparan (alpha = 180) di atas layar gameplay yang dibekukan.
- **Pilihan Tombol:**
  1. `Lanjutkan (Resume)`: Kembali ke `PLAY_STATE`.
  2. `Ulangi Level (Restart)`: Reset state dunia game dan posisi pemain.
  3. `Menu Utama`: Kembali ke `MENU_STATE`.
