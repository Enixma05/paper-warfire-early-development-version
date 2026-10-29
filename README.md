# Paper Warfire

**Paper Warfire** adalah game strategi berbasis giliran (*2D Grid-Based Turn-Based Strategy*) yang mengusung mekanik perencanaan perintah simultan (**WEGO**), kabut perang dinamis (**Fog of War**), dan penargetan serangan koordinat manual dengan visual *Geometric Minimalist 2D* yang terinspirasi dari permainan perang di atas kertas.

Proyek ini dikembangkan menggunakan pendekatan **Spec-Driven Development (SDD)** untuk penugasan mata kuliah Pengembangan Game, yang terbagi ke dalam 2 fase:
- **Phase 1 (Saat Ini - UTS):** Perencanaan ide, cetak biru arsitektur (*Software Design Description*), spesifikasi mekanik, dan rubrik evaluasi.
- **Phase 2 (UAS):** Pengembangan kode modular, kecerdasan buatan (*Rule-Based AI*), integrasi audio-visual, dan pengujian (*testing & revision*).

---

## 🎖️ Acknowledgements & Credit

Proyek ini merupakan pengembangan awal dan adaptasi dari konsep game **Paper Warfire**, yang didasarkan pada ide orisinal serta skripsi/skrip awal yang dirancang oleh:

- **Ide & Konsep Awal:** [@datureksa0045](https://github.com/datureksa0045)

Apresiasi dan ucapan terima kasih kami sampaikan kepada beliau atas fondasi ide pertempuran berbasis koordinat di atas kertas, sistem eksekusi WEGO, dan mekanik taktis yang menjadi inspirasi utama bagi tim dalam merancang game ini.

---

## 🎮 Fitur & Mekanik Utama

1. **Siklus WEGO (Simultaneous Turn Planning):**
   - Pemain dan lawan (AI) menyusun satu perintah utama (`MOVE` atau `ATTACK`) per unit secara rahasia pada *Planning Phase*.
   - Seluruh perintah dieksekusi secara serentak pada *War Phase* (pergerakan $\to$ pengintaian $\to$ pertempuran simultan $\to$ evaluasi).
2. **Kabut Perang (Fog of War):**
   - Membatasi visibilitas medan perang menjadi 3 status: *Unexplored*, *Explored*, dan *Visible*.
   - AI lawan mematuhi batasan kabut perang (*Fog of War compliant AI*) tanpa kecurangan.
3. **Penargetan Koordinat Manual (Blind Firing):**
   - Serangan proyektil dan artileri diarahkan melalui input koordinat manual (angka X/Y atau alfanumerik seperti `H8`).
   - Senjata memiliki area ledakan (*AoE 3x3*) dengan kalkulasi *falloff damage* yang sekaligus membuka kabut perang di titik dampak.
4. **Variasi 6 Kelas Unit Tempur:**
   - *Pistol* (infanteri cepat), *Machine Gun* (supresi area), *Sniper* (jarak jauh akurat), *Tank* (benteng garis depan), *Mortar* (tembakan lengkung), dan *Artillery* (penghancur jarak jauh).
5. **Ekonomi Koin & Upgrade Toko:**
   - Koin diperoleh dari hasil evaluasi giliran untuk membeli upgrade senjata (*Penetration*, *Scope*, *Magazine*, *Scan Drone*).

---

## 📁 Struktur Proyek

```text
Final Project/
├── assets/                     # Aset multimedia game (Role 3)
│   ├── audio/                  # Efek suara (SFX) & musik latar (BGM)
│   ├── fonts/                  # Tipografi TrueType (TTF)
│   └── sprites/                # Gambar unit dan tileset PNG
├── docs/                       # Dokumentasi spesifikasi lengkap (SDD & GDD)
│   ├── concept/                # Kanvas brainstorming ide, mekanik, & audio-visual
│   │   ├── brainstorming.md
│   │   ├── mechanics_sketch.md
│   │   └── visual_audio_ui.md
│   ├── uts/                    # Template dokumen penugasan UTS
│   │   ├── Perencanaan Game.docx
│   │   └── Template_Perencanaan_dan_Rubrik_Game.docx
│   ├── global/                 # Spesifikasi global dan batasan teknis
│   │   ├── PROJECT_SPEC.md
│   │   ├── GAME_DESIGN.md
│   │   ├── TECH_SPEC.md
│   │   └── CONSTRAINTS.md
│   ├── player/                 # Spesifikasi komponen pemain (Role 2)
│   │   ├── movement.md
│   │   ├── health.md
│   │   └── interaction.md
│   ├── enemy/                  # Spesifikasi AI & aturan tempur lawan (Role 2)
│   │   ├── behavior.md
│   │   └── combat.md
│   └── ui/                     # Spesifikasi antarmuka HUD & Menu (Role 3)
│       ├── hud.md
│       ├── menu.md
│       └── game-over.md
├── src/                        # Kode sumber modular game terorganisir per domain
│   ├── core/                   # Engine loop 60 FPS, FSM State Manager, Input Handler (Role 1)
│   ├── game/                   # Grid battlefield, Fog of War, Battle Resolver simultan
│   ├── player/                 # Kontroler skuadron & unit kawan (Role 2)
│   ├── enemy/                  # Rule-Based AI Controller & unit lawan (Role 2)
│   └── ui/                     # Komponen HUD, menu utama, modal jeda, renderer teks (Role 3)
├── tests/                      # Pengujian unit logic terisolasi via Pytest
├── .gitignore                  # Filter pengecualian Git
├── AGENTS.md                   # Panduan operasional & aturan virtual environment bagi AI Agent
├── PANDUAN_ROLE_TIM.md         # Panduan alur kerja tim 3 orang & aturan Git Flow (PR)
├── requirements.txt            # Daftar dependensi Python (pygame, PyYAML, pytest)
├── setup_env.py                # Script otomatis inisialisasi venv 'proyek-gaming'
└── README.md                   # Informasi utama proyek
```

---

## 🛠️ Persiapan Lingkungan & Instalasi

Proyek ini menggunakan **Python 3.12** dengan virtual environment bernama `proyek-gaming`.

Untuk menyiapkan lingkungan kerja secara otomatis:
```bash
# Jalankan script setup otomatis (membuat venv & memasang dependensi)
python setup_env.py
```

### Eksekusi Pengujian:
```bash
# Menjalankan seluruh pengujian unit logika game
.\proyek-gaming\Scripts\python.exe -m pytest tests/
```

---

## 👥 Tim Pengembang & Kolaborasi

Pengerjaan proyek dibagi secara modular ke dalam 3 peran (*Role*):
- **Role 1 (Project Leader & Engine Architect):** Mengelola arsitektur inti (*Game Loop*, *State Manager*, *Clock Delta Time*), review integrasi *Pull Request*, dan stabilitas repositori.
- **Role 2 (Gameplay, Mechanics & AI Programmer):** Mengembangkan mekanik unit, perilaku *Rule-Based AI*, deteksi tabrakan grid, dan resolusi pertempuran simultan.
- **Role 3 (UI/UX Designer, Audio Integrator & QA Tester):** Merancang layout HUD taktis, transisi menu, integrasi aset SFX/BGM, dan eksekusi rencana pengujian (*playtesting*).

*Panduan detail kontribusi dan aturan branch fitur dapat dilihat pada [PANDUAN_ROLE_TIM.md](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/PANDUAN_ROLE_TIM.md).*
