# Batasan & Standar Teknis (CONSTRAINTS.md)

Dokumen ini mendefinisikan batasan teknis lingkungan kerja (*runtime environment*), standar kode pemograman, batas resolusi grafis, performa frame-rate, serta konvensi kolaborasi git untuk game *OPERATION: PHANTOM WIRE*.

---

## 1. Lingkungan Kerja & Dependensi Perangkat Lunak

- **Bahasa Pemrograman:** Python 3.12 (Virtual Environment `proyek-gaming`).
- **Framework Game:** `pygame==2.6.1` (SDL 2.28.x).
  - *Batasan:* Tidak diperkenankan menggunakan engine eksternal seperti Unity, Unreal, atau Godot. Seluruh sistem game loop, raycasting, dan rendering dibangun murni menggunakan Pygame.
- **Parser Konfigurasi Level:** `PyYAML==6.0.3` (Digunakan untuk memuat data waypoint musuh, posisi generator, dan layout koordinat objek dari file `.yaml`).
- **Framework Pengujian Otomatis:** `pytest==9.1.1` (Wajib digunakan di folder `tests/` untuk memverifikasi logika math raycast, kalkulasi damage, dan FSM state).
- **Prosedur Environment:** Inisialisasi otomatis dilakukan melalui script mandiri cross-platform `python setup_env.py` yang membaca referensi dari `requirements.txt`.

---

## 2. Resolusi Layar & Standar Performa Grafis

- **Resolusi Kanvas Rendering Utama:** $1280 \times 720\text{ piksel}$ (Aspek Rasio 16:9 HD).
- **Target Frame Rate:** Stabil di **60 FPS** tanpa fluktuasi yang menyebabkan stuttering visual.
- **Mekanisme Kamera (Viewport Scrolling):**
  - Kamera mengikuti pergerakan karakter pemain (*Lerp Follow Camera*) dengan batas koordinat (*clamping*) sesuai luas peta sektor ($2560 \times 1440\text{ piksel}$).
- **Spesifikasi Format Aset:**
  - **Sprites & Grafis:** Format `.png` 32-bit dengan saluran transparansi *Alpha Channel*. Ukuran tile grid $32 \times 32$ atau $64 \times 64$ piksel.
  - **Audio & Musik:**
    - Sound Effect (SFX): Format `.wav` uncompressed 16-bit 44.1 kHz untuk latensi instan saat ditembakkan.
    - Background Music (BGM): Format `.ogg` atau `.mp3` terkompresi dengan volume dinamis yang diturunkan saat status *Caution/Sneak* dan dinaikkan saat *Alert*.
  - **Tipografi:** Format `.ttf` (TrueType Font) monospaced berlisensi open-source / bebas komersial.

---

## 3. Konvensi Struktur Kode & Kualitas (Coding Standards)

- **Gaya Penulisan:** Mengikuti pedoman resmi **PEP 8**:
  - Nama Kelas: `PascalCase` (contoh: `PatrolGuard`, `StateManager`, `SoundManager`).
  - Nama Fungsi & Method: `snake_case` (contoh: `update_vision_raycast()`, `take_damage()`).
  - Konstanta Global: `SCREAMING_SNAKE_CASE` (contoh: `VIEW_DISTANCE`, `MAX_HEALTH`, `FPS`).
- **Pemisahan Logika & Visual (Testability):**
  - Seluruh kalkulasi matematis (deteksi jarak, persilangan garis pandang raycast, status kalkulasi desibel) harus dipisahkan ke dalam method murni (*pure methods*) tanpa ketergantungan langsung pada `pygame.display` atau jendela aktif, agar dapat diuji secara independen oleh `pytest` di lingkungan CI/CD tanpa membuka jendela GUI.

---

## 4. Konvensi Kolaborasi Git & Integritas Repositori

- **Branching Flow:** Seluruh anggota tim wajib mematuhi aturan di `PANDUAN_ROLE_TIM.md`.
  - Dilarang keras push langsung ke branch `main`.
  - Gunakan branch fitur per role: `feature/core-<fitur>` (Role 1), `feature/player-<fitur>` / `feature/enemy-<fitur>` (Role 2), dan `feature/ui-<fitur>` (Role 3).
- **Penyaringan Repositori (`.gitignore`):**
  - Seluruh cache virtual environment (`proyek-gaming/`, `.venv/`), temporary file Microsoft Word (`~$*.docx`), dan cache pengujian (`.pytest_cache/`) tidak boleh masuk ke riwayat commit Git.
