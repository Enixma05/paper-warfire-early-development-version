# Paper Warfire

**Paper Warfire** adalah game strategi taktis berbasis giliran (*2D Grid-Based Turn-Based Strategy*) yang mengusung mekanik perencanaan perintah simultan (**WEGO**), kabut perang dinamis (**Fog of War**), dan penargetan serangan koordinat manual dengan visual *Geometric Minimalist 2D* yang terinspirasi dari permainan perang di atas kertas buku berpetak.

Proyek ini dikembangkan menggunakan pendekatan **Spec-Driven Development (SDD)** untuk penugasan mata kuliah Pengembangan Game:
- **Phase 1 (Selesai):** Perencanaan ide, cetak biru arsitektur (*Software Design Description*), spesifikasi mekanik, dan rubrik evaluasi.
- **Phase 2 (Saat Ini — Aktif):** Pengembangan kode modular, kecerdasan buatan (*Rule-Based AI*), integrasi audio-visual, dan pengujian otomatis (*automated testing*).

---

## 🎖️ Acknowledgements & Credit

Proyek ini merupakan pengembangan awal dan adaptasi dari konsep game **Paper Warfire**, yang didasarkan pada ide orisinal serta skripsi/skrip awal yang dirancang oleh:

- **Ide & Konsep Awal:** [@datureksa0045](https://github.com/datureksa0045)

Apresiasi dan ucapan terima kasih kami sampaikan kepada beliau atas fondasi ide pertempuran berbasis koordinat di atas kertas, sistem eksekusi WEGO, dan mekanik taktis yang menjadi inspirasi utama bagi tim dalam merancang game ini.

---

## 🎮 Fitur & Mekanik Utama

1. **Siklus WEGO (Simultaneous Turn Planning):**
   - Pemain dan lawan (AI) menyusun satu perintah utama (`MOVE` atau `ATTACK`) per unit secara rahasia pada *Planning Phase*.
   - Seluruh perintah dieksekusi secara serentak pada *War Phase* (pergerakan $\to$ pengintaian $\to$ pertempuran simultan $\to$ evaluasi korban $\to$ pengungkapan kabut).
2. **Kabut Perang Dinamis (Fog of War):**
   - Membatasi visibilitas medan perang menjadi 3 status: *Unexplored* (gelap pekat), *Explored* (redup/terrain diketahui), dan *Visible* (terang penuh dalam jangkauan radar).
   - AI lawan mematuhi batasan kabut perang (*Fog of War compliant AI*) tanpa membaca koordinat tersembunyi pemain.
3. **Penargetan Koordinat Manual (Blind Firing):**
   - Serangan proyektil dan artileri diarahkan melalui input koordinat manual (angka X/Y atau alfanumerik seperti `H8`).
   - Senjata memiliki area ledakan (*AoE 3x3*) dengan kalkulasi *falloff damage* (100% pusat, 50% tepi) yang sekaligus membuka kabut perang di titik dampak.
4. **Variasi 6 Kelas Unit Tempur:**
   - *Pistol* (infanteri pengintai cepat), *Machine Gun* (supresi area), *Sniper* (penembak runduk burst), *Tank* (benteng garis depan ber-armor), *Mortar* (tembakan parabola lengkung), dan *Artillery* (penghancur jarak jauh).
5. **Ekonomi Koin & Upgrade Toko:**
   - Koin diperoleh dari hasil evaluasi giliran, eliminasi unit musuh, dan penjelajahan tile baru untuk membeli upgrade senjata (*Penetration Shells*, *Extended Scope*, *Magazine Upgrade*, *Scan Drone*).

---

## 🚀 Panduan Menjalankan Game

### 1. Prasyarat Lingkungan Kerja
Pastikan Python 3.12+ telah terpasang di komputer Anda. Virtual environment `proyek-gaming` telah dikonfigurasi dengan pustaka `pygame`, `pyyaml`, dan `pytest`.

Jika baru pertama kali melakukan clone atau environment belum terpasang:
```powershell
python setup_env.py
```

### 2. Menjalankan Permainan (GUI Mode)
Jalankan game menggunakan interpreter Python dari virtual environment `proyek-gaming`:

- **Cara Langsung (Rekomendasi Windows):**
  ```powershell
  .\proyek-gaming\Scripts\python.exe main.py
  ```

- **Atau dengan Mengaktifkan Virtual Environment Terlebih Dahulu:**
  ```powershell
  # Aktifkan virtual environment
  .\proyek-gaming\Scripts\Activate.ps1

  # Jalankan game
  python main.py
  ```

### 3. Menjalankan Uji Cepat Smoke-Test (Headless Mode)
Untuk menguji engine game secara cepat di latar belakang tanpa membuka jendela GUI:
```powershell
.\proyek-gaming\Scripts\python.exe main.py --headless
```

---

## 🕹️ Panduan Kontrol & Cara Bermain

| Input / Tombol | Aksi Permainan | Keterangan / Fungsi |
| :--- | :--- | :--- |
| **Klik Kiri Mouse** | Seleksi Unit / Tile | Klik unit kawan (berwarna biru) untuk memilih unit dan membuka panel inspeksi taktis di sebelah kanan. |
| **Tombol `[MOVE]`** | Perintah Gerak | Klik tombol `[MOVE]`, lalu klik salah satu tile yang di-highlight kuning pada grid medan perang. |
| **Tombol `[ATTACK]`** | Perintah Serang | Klik tombol `[ATTACK]`, masukkan koordinat sasaran di kotak input teks (misal: `H8` atau `14, 8`), lalu klik `[CONFIRM]` atau tekan `Enter`. |
| **Blind Bombardment** | Tembakan Buta | Anda dapat menembakkan artileri/tank ke dalam area kabut hitam (*Fog of War*) untuk menebak posisi lawan sekaligus membuka kabut di area $3 \times 3$ sekitar ledakan. |
| **Tombol `[CANCEL]`** | Batal Perintah | Menghapus antrean perintah pada unit yang sedang dipilih. |
| **Tombol `[READY]`** | Eksekusi Fase Perang | Mengunci seluruh perintah yang telah disusun dan memulai **War Phase** serentak bersama musuh. |
| **WASD / Tombol Panah** | Geser Kamera (*Pan*) | Menggeser tampilan medan perang grid $24 \times 16$ tile secara bebas. |
| **Escape / P** | Menu Jeda (*Pause*) | Membuka modal jeda untuk melanjutkan pertandingan, memulai ulang (*restart*), atau kembali ke menu utama. |

---

## 🎨 Penanganan Aset Visual & Audio (Aset Manual / Sementara)

Game saat ini dirancang menggunakan sistem **aset manual built-in bawaan kode** (*procedural minimalist vector graphics*) agar dapat dimainkan secara utuh dan stabil tanpa dependensi file eksternal yang hilang:

- **Visual Saat Ini:** Menggunakan gambar geometri vektor minimalis prosedural dengan pembeda warna taktis (Biru = Kawan, Merah = Lawan, Kuning = Seleksi/Target), palet terrain warna kertas militer, dan mini health bar adaptif.
- **Rencana Penambahan Aset Manual oleh Tim:**
  Pemain dan rekan tim nantinya dapat menambahkan aset kustom secara mandiri ke direktori berikut:
  - `assets/sprites/`: Tempat meletakkan file `.png` (misal: `pistol.png`, `machine_gun.png`, `sniper.png`, `tank.png`, `mortar.png`, `artillery.png`). Engine otomatis mendeteksi dan memuat sprite tersebut jika ada, serta secara halus beralih ke gambar geometri manual jika file belum tersedia.
  - `assets/audio/`: Tempat meletakkan file `.wav` / `.ogg` / `.mp3` (misal: `shot.wav`, `explosion.wav`, `click.wav`, `bgm.ogg`). Sistem audio dirancang dengan *silent fallback* sehingga tidak akan menimbulkan crash jika audio belum ditambahkan.
  - `assets/fonts/`: Tempat meletakkan file tipografi `.ttf` kustom.

---

## 🧪 Eksekusi Pengujian Otomatis (Pytest)

Game ini memiliki 16 pengujian unit otomatis yang mencakup seluruh logika grid, Fog of War, resolusi benturan serentak, formula damage falloff AoE, kepatuhan AI tanpa curang, dan syarat kemenangan/kekalahan:

```powershell
.\proyek-gaming\Scripts\python.exe -m pytest tests/
```

Contoh output yang diharapkan:
```text
============================= test session starts =============================
collected 16 items

tests\test_battle_resolver.py ...                                        [ 18%]
tests\test_battlefield.py ....                                           [ 43%]
tests\test_enemy_ai.py ....                                              [ 68%]
tests\test_fog_of_war.py ..                                              [ 81%]
tests\test_rules_and_win_conditions.py ...                               [100%]

============================= 16 passed in 0.10s ==============================
```

---

## 📁 Struktur Proyek

```text
video-game/
├── main.py                     # Entry point eksekusi game (GUI & --headless)
├── assets/                     # Aset multimedia (Akan ditambahkan bertahap oleh tim)
│   ├── audio/                  # Efek suara (SFX) & musik latar (BGM)
│   ├── fonts/                  # Tipografi TrueType (.ttf)
│   └── sprites/                # Sprite unit & terrain (.png)
├── docs/                       # Dokumentasi spesifikasi lengkap (SDD & GDD)
│   ├── concept/                # Brainstorming ide, mekanik, & audio-visual
│   ├── uts/                    # Dokumen deliverables UTS (Perencanaan Game.docx)
│   ├── global/                 # Spesifikasi global (PROJECT_SPEC, GAME_DESIGN, TECH_SPEC, CONSTRAINTS)
│   ├── player/                 # Spesifikasi entitas kawan (movement, health, interaction)
│   ├── enemy/                  # Spesifikasi AI & tempur lawan (behavior, combat)
│   └── ui/                     # Spesifikasi antarmuka HUD & Menu
├── src/                        # Kode sumber modular game terorganisir per domain
│   ├── core/                   # Engine 60 FPS, FSM State Manager, Input Handler, Audio Manager
│   ├── game/                   # Config terpusat, Grid Battlefield, Fog of War, Battle Resolver simultan
│   ├── player/                 # Kontroler skuadron & unit kawan
│   ├── enemy/                  # Rule-Based AI Controller & unit lawan
│   └── ui/                     # Komponen HUD in-game, input koordinat, Menu, Modal Pause, Game Over
├── tests/                      # Pengujian unit logic terisolasi via Pytest
├── .gitignore                  # Filter pengecualian Git
├── AGENTS.md                   # Panduan operasional & aturan virtual environment bagi AI Agent
├── PANDUAN_ROLE_TIM.md         # Panduan alur kerja tim 3 orang & aturan Git Flow (PR)
├── requirements.txt            # Daftar dependensi Python (pygame, PyYAML, pytest)
├── setup_env.py                # Script otomatis inisialisasi venv 'proyek-gaming'
└── README.md                   # Dokumentasi utama proyek
```

---

## 👥 Tim Pengembang & Kolaborasi

- **Role 1 (Project Leader & Engine Architect):** Mengelola arsitektur inti (*Game Loop*, *State Manager*, *Clock Delta Time*), review integrasi *Pull Request*, dan stabilitas repositori.
- **Role 2 (Gameplay, Mechanics & AI Programmer):** Mengembangkan mekanik unit, perilaku *Rule-Based AI*, deteksi tabrakan grid, dan resolusi pertempuran simultan.
- **Role 3 (UI/UX Designer, Audio Integrator & QA Tester):** Merancang layout HUD taktis, transisi menu, integrasi aset SFX/BGM, dan eksekusi rencana pengujian (*playtesting*).

*Panduan detail kontribusi dan aturan branch fitur dapat dilihat pada [PANDUAN_ROLE_TIM.md](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/PANDUAN_ROLE_TIM.md).*
