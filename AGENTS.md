# AGENTS.md — Instruksi & Panduan Operasional AI Agent

Dokumen ini mendefinisikan aturan dan petunjuk bagi AI Agent dalam menjalankan perintah, mengeksekusi script/tes, serta mengelola dependensi proyek game ini.

---

## 1. Environment & Eksekusi Python

Proyek ini menggunakan **Virtual Environment** bernama `proyek-gaming` yang merujuk pada [`requirements.txt`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/requirements.txt).
Script inisialisasi otomatis disediakan melalui [`setup_env.py`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/setup_env.py).

### Aturan Inisialisasi & Eksekusi bagi AI Agent:
1. **Inisialisasi Environment Otomatis:**
   Jika environment belum tersedia di mesin lokal atau paket belum terpasang, jalankan:
   ```powershell
   python setup_env.py
   ```
   Script ini akan mendeteksi (atau membuat) venv `proyek-gaming` dan menginstal seluruh isi `requirements.txt`.

2. **Aturan Eksekusi Perintah Python & Pytest:**
   Selalu gunakan Python dari virtual environment `proyek-gaming`:
   - **Jika menggunakan Conda:**
     ```powershell
     C:\Users\<Username>\miniconda3\envs\proyek-gaming\python.exe <script.py>
     ```
   - **Jika menggunakan venv lokal di root:**
     ```powershell
     .\proyek-gaming\Scripts\python.exe <script.py>
     ```
   - **Pytest:**
     ```powershell
     <path_ke_proyek-gaming_python> -m pytest tests/
     ```

---

## 2. Aturan Pengelolaan Dependensi

### A. Prosedur Wajib Pra-Eksekusi Kode (Pre-execution Check):
Sebelum mengeksekusi script game, modul baru, atau test runner:
1. **Analisis Import/Modul Baru:**
   Periksa apakah kode membutuhkan package eksternal selain standard library Python dan dependensi saat ini (`pygame`, `pyyaml`, `pytest`).
2. **Cek Ketersediaan Modul:**
   Uji terlebih dahulu di environment `proyek-gaming`:
   ```powershell
   <path_ke_proyek-gaming_python> -c "import <nama_package>"
   ```
3. **Instalasi Sebelum Eksekusi:**
   Jika modul belum terpasang (`ModuleNotFoundError`), pasang paket ke environment `proyek-gaming` terlebih dahulu sebelum menjalankan kode utama.

### B. Prosedur Penambahan Dependensi Baru:
Jika agen atau pengguna menambahkan package/library baru ke proyek:
1. **Wajib Memasang ke Environment `proyek-gaming`:**
   ```powershell
   <path_ke_proyek-gaming_python> -m pip install <nama_package>
   ```
2. **Wajib Memperbarui [`requirements.txt`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/requirements.txt):**
   - Tambahkan nama package dan versinya ke `requirements.txt` agar rekan tim lain langsung mendapatkan dependensi yang sama saat menjalankan `python setup_env.py`.

---

## 3. Struktur Direktori & Konvensi Kode

- `src/core/`: Logika loop utama, FSM State Manager, Delta Clock, Input Handler.
- `src/game/`: Aturan permainan, collision logic, level loader, spawner.
- `src/player/`: Entitas playable character, movement, health, interaction.
- `src/enemy/`: Entitas musuh, AI patroli/mengejar, boss mechanics.
- `src/ui/`: Komponen HUD, Menu, modal, font rendering.
- `assets/`: 
  - `assets/sprites/` untuk gambar/sprite.
  - `assets/audio/` untuk SFX dan BGM.
  - `assets/fonts/` untuk tipografi.
- `PANDUAN_ROLE_TIM.md`: Panduan alur kerja dan pembagian tugas 3 anggota tim.
- `docs/`: 
  - `docs/uts/`: Template perencanaan UTS (`Perencanaan Game.docx`).
  - `docs/global/`, `docs/player/`, `docs/enemy/`, `docs/ui/`: Spesifikasi SDD granular.

---

## 4. Alur Kerja Proyek (2 Phase)

- **Phase 1 (Saat Ini): Perencanaan & SDD (UTS):**
  - Jangan menulis kode game sebelum spesifikasi di `docs/uts/Perencanaan Game.docx` dan dokumen SDD disepakati.
  - Bantu tim mengisi arsitektur loop, state, struktur kelas, dan kriteria rubrik teknis & UX.
- **Phase 2: Pengembangan, Testing & Revisi:**
  - Kembangkan kode secara modular per domain (`src/core`, `src/player`, dll.).
  - Setiap fitur baru harus disertai pengujian di folder `tests/` menggunakan `pytest`.
