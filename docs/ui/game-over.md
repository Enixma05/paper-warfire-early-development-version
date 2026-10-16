# Spesifikasi Layar Akhir Game (game-over.md)

Spesifikasi antarmuka Game Over (Kalah) dan Layar Kemenangan (Victory Screen).

---

## 1. Layar Kalah (Game Over)
- **Kondisi Muncul:** Dipicu ketika `player.current_health <= 0`.
- **Elemen Tampilan:**
  - Teks Utama: `GAME OVER` berwarna merah tajam.
  - Skor Akhir: `Skor Kamu: [XXXX]`.
  - Tombol Pilihan:
    - `Coba Lagi (Retry)`: Reset permainan langsung dari awal level.
    - `Kembali ke Menu`: Transisi ke `MENU_STATE`.
- **Audio Feedback:** Memutar SFX kekalahan singkat yang dramatis.

## 2. Layar Menang (Victory / Stage Clear)
- **Kondisi Muncul:** Dipicu saat syarat menang terpenuhi (Boss akhir dikalahkan).
- **Elemen Tampilan:**
  - Teks Utama: `VICTORY!` / `MISI SELESAI` berwarna emas/hijau cerah.
  - Rincian Statistik:
    - Waktu Bertahan / Waktu Tempuh: `MM:SS`
    - Total Musuh Dikalahkan: `X musuh`
    - Skor Akhir Terakumulasi: `XXXXX pts`
  - Tombol Pilihan:
    - `Main Lagi`: Memulai ulang permainan.
    - `Menu Utama`: Kembali ke halaman depan.
- **Audio Feedback:** Memutar lagu kemenangan (Victory Fanfare).
