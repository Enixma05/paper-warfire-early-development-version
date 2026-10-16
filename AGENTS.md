# AGENTS.md — Instruksi & Panduan Operasional AI Agent

Dokumen ini mendefinisikan aturan dan petunjuk bagi AI Agent dalam menjalankan perintah, mengeksekusi script/tes, serta mengelola dependensi proyek game ini.

---

## 1. Environment & Eksekusi Python

Proyek ini menggunakan **Conda Environment** khusus bernama `proyek-gaming` (Python 3.12).
Referensi pembuatan dan aktivasi environment tercatat pada [`set-up env.bat`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/set-up%20env.bat).

### Aturan Eksekusi Python & Command Line:
1. **Gunakan Python dari Environment `proyek-gaming`:**
   Saat menjalankan perintah terminal (PowerShell / Command Prompt), panggil interpreter python melalui path absolut env atau condabin:
   - **Python Executable:**
     ```powershell
     C:\Users\ASUS\miniconda3\envs\proyek-gaming\python.exe <script.py>
     ```
   - **Pip Executable:**
     ```powershell
     C:\Users\ASUS\miniconda3\envs\proyek-gaming\python.exe -m pip <command>
     ```
   - **Pytest:**
     ```powershell
     C:\Users\ASUS\miniconda3\envs\proyek-gaming\python.exe -m pytest tests/
     ```
2. **Jangan gunakan Python sistem global** (`Python313`) tanpa mengaktifkan env, karena paket inti (`pygame`, `pyyaml`, `pytest`) terpasang di `proyek-gaming`.

---

## 2. Aturan Pengelolaan Dependensi

### A. Prosedur Wajib Pra-Eksekusi Kode (Pre-execution Check):
Sebelum mengeksekusi script game, modul baru, atau test runner:
1. **Analisis Import/Modul Baru:**
   Periksa apakah kode membutuhkan package eksternal selain standard library Python dan dependensi saat ini (`pygame`, `pyyaml`, `pytest`).
2. **Cek Ketersediaan Modul:**
   Jika ada import pihak ketiga yang baru atau belum dipastikan terpasang, uji terlebih dahulu di environment `proyek-gaming`:
   ```powershell
   C:\Users\ASUS\miniconda3\envs\proyek-gaming\python.exe -c "import <nama_package>"
   ```
3. **Instalasi Sebelum Eksekusi:**
   Jika modul belum terpasang (`ModuleNotFoundError`), pasang paket terlebih dahulu sebelum menjalankan kode utama.

### B. Prosedur Penambahan Dependensi Baru:
Jika agen atau pengguna menambahkan package/library baru ke proyek:
1. **Wajib Memasang ke Environment `proyek-gaming`:**
   ```powershell
   C:\Users\ASUS\miniconda3\envs\proyek-gaming\python.exe -m pip install <nama_package>
   ```
2. **Wajib Memperbarui [`requirements.txt`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/requirements.txt):**
   - Perbarui daftar dependensi agar versi tetap sinkron dan reproducible:
     ```powershell
     C:\Users\ASUS\miniconda3\envs\proyek-gaming\python.exe -m pip freeze > requirements.txt
     ```
3. **Wajib Memperbarui [`set-up env.bat`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/set-up%20env.bat):**
   - Tambahkan nama package baru ke baris instalasi pip pada file batch:
     ```cmd
     python -m pip install pytest pyyaml pygame <nama_package_baru>
     ```
   - Hal ini memastikan rekan tim lain yang menjalankan `set-up env.bat` langsung mendapatkan dependensi yang sama secara otomatis.

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
