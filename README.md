# Game Project

Proyek game sederhana menggunakan Spec-Driven Development (SDD).

## Struktur Proyek
- `PANDUAN_ROLE_TIM.md`: Panduan alur kerja dan pembagian peran 3 anggota tim
- `docs/`: Spesifikasi proyek & dokumen perencanaan (SDD/GDD):
  - `docs/concept/`: Kanvas brainstorming ide, mekanik, dan konsep visual/audio tim
  - `docs/uts/`: Template dokumen penugasan UTS (`Perencanaan Game.docx`)
  - `docs/global/`: Spesifikasi teknis, game design, project scope, dan constraints
  - `docs/player/`, `docs/enemy/`, `docs/ui/`: Detail modular SDD tiap komponen game
- `src/`: Source code game terorganisir per domain:
  - `src/core/`: Engine inti, Game Loop, State Manager, Input Handler (Role 1)
  - `src/player/`: Logika dan controller pemain (Role 2)
  - `src/enemy/`: Logika musuh dan AI (Role 2)
  - `src/game/`: Logika level, rule manager, collision & spawner (Role 1 & 2)
  - `src/ui/`: Komponen visual UI, menu, dan HUD (Role 3)
- `assets/`: Aset multimedia (sprites, audio, fonts) (Role 3)
- `tests/`: Pengujian unit dan skenario game

