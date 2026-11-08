# Batasan & Standar Teknis (CONSTRAINTS.md)

Dokumen ini mendefinisikan batasan teknis lingkungan kerja (*environment*), standar performa, format aset, serta konvensi pemrograman yang wajib dipatuhi seluruh anggota tim dalam pengembangan **Paper Warfire**.

---

## 1. Lingkungan Pengembangan & Eksekusi (Environment)
- **Bahasa Pemrograman:** Python 3.12 (Virtual Environment `proyek-gaming`).
- **Framework Utama:** Pygame 2.6.x (SDL 2.28.x).
  - *Catatan:* Tidak menggunakan engine eksternal berbayar; seluruh logika grid, Fog of War, dan rendering dibangun dari nol di atas Pygame sesuai rubrik teknis kuliah.
- **Pengelola Dependensi:** `requirements.txt` dan script otomatis [`setup_env.py`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/setup_env.py).
- **Pengujian Unit & Logika:** `pytest` (versi 9.x).
- **Format File Konfigurasi Data:** YAML (`pyyaml`) untuk data atribut unit dan seed terrain peta.

---

## 2. Resolusi Layar & Standar Performa
- **Resolusi Jendela Standar:** $1280 \times 720$ piksel (Aspek Rasio 16:9 HD).
- **Ukuran Grid Layar:**
  - Area Battlefield: $24 \times 16$ tile.
  - Ukuran Per Tile: $40 \times 40$ piksel (Total grid $960 \times 640$ piksel).
  - Area Sisa ($320$ px samping & $80$ px atas/bawah): Didedikasikan untuk HUD, Panel Perintah, dan Input Koordinat.
- **Target Frame Rate:** 60 FPS stabil dengan konsumsi CPU rendah.
- **Penggunaan Memori (RAM):** Di bawah 250 MB saat runtime.

---

## 3. Standar & Format Aset Multimedia
Aset visual dan audio dirancang ringan dan bertema minimalis militer di atas kertas:
- **Aset Visual:**
  - Format: `.png` dengan transparansi alpha penuh (32-bit RGBA).
  - Gaya Visual: *Geometric Minimalist 2D* (garis bersih, palet kontras tinggi, simbol taktis militer).
- **Aset Audio:**
  - Sound Effects (SFX): `.wav` / `.ogg` dengan durasi pendek (< 3 detik), sample rate 44.1 kHz.
  - Music (BGM): `.ogg` / `.mp3` looping tanpa jeda klik (*seamless loop*).
  - Audio Leveling: Efek suara tidak boleh menutupi BGM, dan BGM dapat diatur volumenya melalui menu pengaturan.
- **Tipografi:**
  - Format: `.ttf` (TrueType Font) bergaya sans-serif / monospace modern yang mudah dibaca di berbagai resolusi layar.

---

## 4. Konvensi Pemrograman & Gaya Kode (Code Style)
- **Standar Standar:** Mengikuti panduan **PEP 8**:
  - Nama Kelas: `PascalCase` (contoh: `BattlefieldGrid`, `PlayerController`).
  - Nama Fungsi & Variabel: `snake_case` (contoh: `calculate_damage()`, `unit_list`).
  - Konstanta Global: `SCREAMING_SNAKE_CASE` (contoh: `MAX_HEALTH`, `TARGET_FPS`).
- **Prinsip Modularitas (Separation of Concerns):**
  - Modul logika tempur tidak boleh mengandung fungsi render Pygame langsung (`pygame.draw` atau `screen.blit`).
  - Semua modul logika harus dapat dijalankan secara headless untuk keperluan pengujian otomatis Pytest.
- **Penanganan Konflik Git:**
  - Seluruh anggota tim wajib mematuhi aturan Git Flow pada [`PANDUAN_ROLE_TIM.md`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/PANDUAN_ROLE_TIM.md) dengan bekerja di branch fitur masing-masing dan membuat Pull Request sebelum penggabungan ke branch `main`.
