# Project Specification: Paper Warfire (PROJECT_SPEC.md)

Dokumen ini mendefinisikan batas cakupan (*scope*), arsitektur permainan tingkat tinggi, serta kriteria keberhasilan untuk **Paper Warfire** pada Phase 1 (Perencanaan UTS) dan Phase 2 (Implementasi UAS).

---

## 1. Identitas & High Concept Proyek
- **Judul Game:** Paper Warfire
- **Genre:** 2D Grid-Based Turn-Based Strategy (Mekanik WEGO & Fog of War)
- **Perspektif Visual:** Top-Down 2D Geometric Minimalist
- **Inspirasi Utama:** Frozen Synapse (pendekatan WEGO simultaneous), Advance Wars (taktik grid & variasi unit), Age of Empires (Fog of War & pengintaian), serta Battleship / Perang Kertas klasik.
- **Target Platform:** Desktop PC (Windows / Cross-platform Linux & macOS)
- **Teknologi Utama:** Python 3.12, Pygame 2.6.x

---

## 2. Ruang Lingkup Proyek (Scope of Work)

### A. Phase 1: Perencanaan & Software Design Description (Target UTS)
1. **Arsitektur Game Loop & State Machine (FSM):**
   - Merancang siklus dua fase inti: `Planning Phase` (penyusunan perintah simultan) dan `War Phase` (resolusi pergerakan dan serangan simultan).
   - Memetakan FSM global (`MENU`, `PLAY_PLANNING`, `PLAY_WAR`, `TURN_SUMMARY`, `PAUSE`, `VICTORY`, `DEFEAT`).
2. **Struktur Berorientasi Objek (OOP) & Data Models:**
   - Desain modul terpisah: `core/`, `player/`, `enemy/`, `game/`, dan `ui/`.
   - Spesifikasi kelas entitas unit, grid map, fog of war manager, dan command resolver.
3. **Mekanik & Formula Kuantitatif:**
   - Perumusan atribut lengkap 7 arketipe unit (*Pistol, Machine Gun, Sniper, Tank, Mortar, Artillery, Grenade*).
   - Formula kalkulasi damage, distance falloff AoE 3x3, dan pengali pertahanan terrain.
   - Aturan menang (*eliminasi seluruh unit lawan*) dan kalah (*seluruh unit pemain musnah*).
4. **Penyelarasan Rubrik UTS:**
   - Dokumen perencanaan `docs/uts/Perencanaan Game.docx` siap uji memenuhi seluruh indikator teknis dan pengalaman pengguna (UX).

### B. Phase 2: Pengembangan, Pengujian & Revisi (Target UAS)
1. **Engine Grid & Fog of War:**
   - Grid koordinat dinamis dengan sistem tile layer (Terrain, Unit, Fog of War, Selection/Target Indicator).
   - Algoritma visibilitas kabut perang dan mekanisme pengungkapan tile via dampak serangan (*impact reveal*).
2. **Controller & Rule-Based AI:**
   - Player input interface: pemilihan unit, input koordinat target, dan daftar antrean perintah (*command list*).
   - Rule-based AI opponent yang mematuhi Fog of War tanpa curang (*Fog of War compliant AI*).
3. **Battle Resolver (Simultaneous Execution):**
   - Urutan eksekusi War Phase: Movement $\to$ Recon $\to$ Simultaneous Combat $\to$ Casualty Check $\to$ Fog Update.
4. **Ekonomi Giliran & Upgrade:**
   - Sistem perolehan koin per giliran dan menu upgrade sederhana (*Penetration, Scope, Magazine*).
5. **Quality Assurance & Testing:**
   - Unit testing logika pertempuran dan validasi koordinat menggunakan `pytest`.

---

## 3. Batasan di Luar Cakupan (Out of Scope)
Untuk memastikan penyelesaian proyek tepat waktu dengan kualitas tinggi, fitur berikut ditetapkan di luar cakupan:
- **Online Multiplayer Jaringan:** Fokus murni pada mode Single Player (Pemain Manusia vs Rule-Based AI) atau Hotseat lokal.
- **Sistem Animasi 3D / Rigging Kompleks:** Game menggunakan representasi geometri minimalis top-down 2D.
- **Micro-transaction & Cloud Database:** Seluruh state berjalan lokal selama sesi pertandingan.
- **Fitur Level Editor Eksternal yang Rumit:** Peta medan perang dibangkitkan secara prosedural (*procedural random grid generation*) berdasarkan konfigurasi seed dan tipe terrain.
