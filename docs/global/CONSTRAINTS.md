# Batasan & Standar Teknis (CONSTRAINTS.md)

Aturan teknis, konvensi lingkungan kerja, dan batasan performa sistem.

---

## 1. Environment & Library
- **Bahasa:** Python 3.12 (Conda env `proyek-gaming`).
- **Framework:** Pygame 2.6.x (tidak menggunakan engine pihak ketiga seperti Unity atau Godot).
- **Format Data Konfigurasi:** YAML (`pyyaml`) untuk data level dan atribut entitas.
- **Testing Framework:** `pytest` untuk unit test logika game.

## 2. Resolusi Layar & Performa
- **Resolusi Standar:** 1280 x 720 piksel (16:9 HD) atau 960 x 540 (Retro scalable).
- **Target Frame Rate:** 60 FPS stabil tanpa screen tearing.
- **Asset Formats:**
  - Gambar: `.png` dengan transparansi alpha.
  - Audio: `.wav` untuk SFX pendek, `.ogg` / `.mp3` untuk BGM.
  - Font: `.ttf` (TrueType Font).

## 3. Konvensi Kode
- Gaya penulisan mengikuti PEP 8 (nama kelas `PascalCase`, fungsi dan variabel `snake_case`).
- Seluruh dependensi baru wajib disinkronkan ke `requirements.txt` dan `set-up env.bat`.
