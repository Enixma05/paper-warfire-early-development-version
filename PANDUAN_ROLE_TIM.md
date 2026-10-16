# Panduan Pembagian Tugas & Peran Tim (Team Role Guide)

Dokumen ini berisi petunjuk kerja, pembagian tanggung jawab, aturan alur kerja Git (Branching & Pull Request), serta alur kolaborasi untuk pengerjaan proyek game antar 3 anggota tim, mencakup **Phase 1 (Perencanaan/SDD)** dan **Phase 2 (Pengembangan, Testing & Revisi)**.

---

## Ringkasan Pembagian Role

| Role | Penanggung Jawab | Fokus Utama | Target Phase 1 (Perencanaan) | Target Phase 2 (Pengembangan & Testing) |
| :--- | :--- | :--- | :--- | :--- |
| **Role 1** | **Project Leader & Lead Programmer** | Arsitektur dasar, Game Loop, State Manager, Code Review | Arsitektur Game Loop & State Management di SDD | Implementasi Main Loop, State Manager, Input Handler, & Review Pull Request |
| **Role 2** | **Gameplay, Mechanics & AI Programmer** | Karakter, musuh, combat, aturan game | Spesifikasi Kelas Entitas & Logika Menang/Kalah di SDD | Coding Player controller, Enemy AI, Spawner, & Collision Detection |
| **Role 3** | **UI/UX Designer, Audio & QA (Tester)** | Antarmuka pemain, audio-visual feedback, pengujian | Wireframe UI, Asset Inventory, & Rubrik UX di SDD | Implementasi HUD, Menu, Integrasi SFX/BGM, & Eksekusi Test Plan |

---

## Aturan Git Flow: Pencegahan Konflik (Merge Conflict)

Untuk menjaga stabilitas kode bersama, seluruh anggota tim wajib mematuhi protokol integrasi kode berikut:

> [!IMPORTANT]
> **Aturan Emas:** Dilarang keras melakukan `git push` langsung ke branch `main`! Setiap anggota tim wajib bekerja di branch fitur masing-masing dan membuat **Pull Request (PR)**. Branch `main` hanya dapat diperbarui melalui merge PR yang telah direview oleh **Role 1 (Project Leader)**.

### 1. Standar Penamaan Branch Fitur
Gunakan format nama branch yang konsisten:
- Role 1 (Core): `feature/core-<nama-fitur>` (contoh: `feature/core-state-manager`)
- Role 2 (Gameplay): `feature/player-<fitur>` atau `feature/enemy-<fitur>` (contoh: `feature/player-movement`, `feature/enemy-patrol`)
- Role 3 (UI/Audio): `feature/ui-<fitur>` atau `feature/audio-<fitur>` (contoh: `feature/ui-hud`, `feature/audio-sfx`)
- Perbaikan bug: `fix/<nama-bug>`

### 2. Alur Kerja Harian Tiap Anggota Tim

```
[Branch main] ──(git pull)──► Buat Branch Baru ──► Tulis Kode & Commit ──► Push ke Remote ──► Buka Pull Request (PR) ──► Review by Leader ──► Merge ke main
```

#### Langkah Teknis Tiap Anggota:
1. **Selalu sinkronkan branch lokal sebelum mulai bekerja:**
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Buat branch baru untuk tugas spesifik sesuai role masing-masing:**
   ```bash
   git checkout -b feature/<nama-fitur>
   ```
3. **Commit perubahan secara berkala dengan pesan yang jelas:**
   ```bash
   git add .
   git commit -m "feat(<scope>): penjelasan singkat perubahan"
   ```
4. **Push branch fitur ke remote repository:**
   ```bash
   git push -u origin feature/<nama-fitur>
   ```
5. **Buat Pull Request (PR) di GitHub/GitLab:**
   - Arahkan target branch ke `main`.
   - Berikan deskripsi ringkas mengenai fitur yang dibuat atau diuji.
   - Tetapkan **Role 1 (Project Leader)** sebagai *Reviewer*.
6. **Review & Merge oleh Role 1 (Project Leader):**
   - Role 1 memeriksa keselarasan arsitektur, ketiadaan bentrok, dan standar kode.
   - Jika sudah sesuai, Role 1 menyetujui dan melakukan **Merge Pull Request** ke `main`.

---

## Detail Tanggung Jawab & Petunjuk Pengerjaan

### 1. Role 1: Project Leader & Lead Programmer
*Penanggung jawab pondasi teknis, siklus hidup aplikasi, stabilitas struktur kode, dan review merge.*

- **Phase 1 — Yang Harus Dikerjakan di `Perencanaan Game.docx`:**
  - [ ] **Bab 1 (Arsitektur & Alur Game):**
    - Mendefinisikan diagram/alur siklus **Main Game Loop** (Input $\to$ Update $\to$ Render).
    - Menjelaskan State Machine: fungsi dan transisi antar state (`MENU_STATE`, `PLAY_STATE`, `PAUSE_STATE`, `END_STATE`).
  - [ ] **Rubrik Penilaian Teknis:**
    - Mempersiapkan jawaban dan bukti konsep untuk indikator: *Pemahaman Main Game Loop* dan *Manajemen State*.
  - [ ] **Manajemen Tim:**
    - Memandu pembagian tugas dan menyatukan draf dari Role 2 & Role 3 ke dokumen final `Perencanaan Game.docx`.

- **Phase 2 — Yang Dikerjakan saat Coding:**
  - Membangun struktur modular kode di folder `src/core/`.
  - Mengatur clock/delta time untuk stabilisasi frame rate (FPS).
  - Mengelola transisi scene secara halus tanpa memory leak.
  - **Code Review**: Memeriksa setiap Pull Request dari Role 2 dan Role 3 sebelum digabungkan ke `main`.

---

### 2. Role 2: Gameplay, Mechanics & AI Programmer
*Penanggung jawab logika permainan, rasa bermain (game feel), dan kecerdasan buatan.*

- **Phase 1 — Yang Harus Dikerjakan di `Perencanaan Game.docx`:**
  - [ ] **Bab 2 (Struktur Kelas & Objek):**
    - Merancang atribut dan method untuk entitas: `Player`, `Enemy`, `Obstacle`, `Boss`.
    - Merumuskan formula mekanik (kecepatan gerak, sistem hit point/damage, power-up, dsb.).
  - [ ] **Aturan Permainan & Kondisi Selesai:**
    - Menuliskan skenario detail kondisi Menang (Win Condition) dan Kalah (Lose Condition).
  - [ ] **Rubrik Penilaian Teknis:**
    - Mempersiapkan jawaban dan bukti kode untuk indikator: *Struktur Objek (OOP/ECS)*, *Logika Interaksi & Menang/Kalah*, dan *Tingkat Kerumitan Game*.

- **Phase 2 — Yang Dikerjakan saat Coding:**
  - Bekerja di branch fitur khusus (misal: `feature/player-mechanics`, `feature/enemy-ai`).
  - Coding pergerakan pemain (movement, jump, attack, action) di folder `src/player/`.
  - Coding perilaku musuh (patroli, mengejar pemain, menyerang) di folder `src/enemy/`.
  - Menghubungkan interaksi benturan (collision) antara peluru, musuh, dan obstacle.
  - Membuat Pull Request ke `main` setiap kali fitur selesai diuji.

---

### 3. Role 3: UI/UX Designer, Audio/Asset Integrator & QA (Tester)
*Penanggung jawab keterbacaan visual, umpan balik interaksi, dan kelayakan uji pengguna.*

- **Phase 1 — Yang Harus Dikerjakan di `Perencanaan Game.docx`:**
  - [ ] **Bab 2 (Elemen UI & Status Indikator):**
    - Merancang layout HUD (tampilan darah, skor, status misi, tombol pause).
    - Menyiapkan daftar kebutuhan aset grafis & suara di `docs/` (gambar sprite, audio SFX/BGM).
  - [ ] **Bab 4 (Rubrik Penilaian UX):**
    - Mengisi panduan evaluasi pengalaman bermain: kejelasan tujuan dalam 1 menit pertama, kejelasan visual antara entitas vs background, responsivitas kontrol, dan pencegahan frustrasi.

- **Phase 2 — Yang Dikerjakan saat Coding & Testing:**
  - Bekerja di branch fitur khusus (misal: `feature/ui-menu`, `feature/ui-hud`).
  - Implementasi tampilan UI di folder `src/ui/` (Main Menu, HUD In-Game, Layar Pause, Layar Game Over/Victory).
  - Menghubungkan efek suara (SFX) saat klik tombol, memukul musuh, terluka, atau menang.
  - Membuat dan mengeksekusi skenario uji coba (Playtesting) serta mencatat bug untuk diperbaiki bersama Role 1 dan Role 2.
  - Membuat Pull Request ke `main` saat komponen UI/Audio siap diintegrasikan.
