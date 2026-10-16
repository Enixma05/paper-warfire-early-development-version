# Project Specification (PROJECT_SPEC.md)

Dokumen ini mendefinisikan batasan umum proyek, ruang lingkup pengerjaan, dan target capaian UTS (Phase 1) serta Final Project (Phase 2).

---

## 1. Identitas Proyek
- **Nama Game:** [Isi Judul Game]
- **Genre:** [Isi Genre]
- **Target Platform:** Desktop PC (Windows)
- **Teknologi Utama:** Python 3.12, Pygame 2.6.x

## 2. Ruang Lingkup Proyek (Scope)
- **Phase 1 (UTS - Perencanaan & SDD):**
  - Desain arsitektur Game Loop & State Management FSM.
  - Struktur kelas entitas (OOP).
  - Sketsa formula mekanik & syarat menang/kalah kuantitatif.
  - Pemenuhan kriteria rubrik teknis & UX pada dokumen `docs/uts/Perencanaan Game.docx`.
- **Phase 2 (UAS - Implementasi & Testing):**
  - Pembuatan prototipe fungsional (playable game).
  - Implementasi AI musuh, sistem collision, dan audio feedback.
  - Pengujian modular via Pytest.

## 3. Batasan di Luar Cakupan (Out of Scope)
- Fitur Online Multiplayer / Jaringan (Game difokuskan pada Single Player lokal).
- Sistem Save/Load database cloud yang kompleks.
