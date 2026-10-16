# Technical Specification (TECH_SPEC.md)

Spesifikasi teknis arsitektur perangkat lunak game, pola desain, dan alur eksekusi (Tanggung Jawab Role 1).

---

## 1. Arsitektur Game Loop
- **Target FPS:** 60 FPS (dibatasi menggunakan `pygame.time.Clock()`).
- **Penerapan Delta Time (`dt`):** Seluruh kalkulasi pergerakan fisik menggunakan perkalian `dt` (detik) untuk menjamin pergerakan konsisten di berbagai spesifikasi PC.
- **Siklus Loop:**
  1. `process_events()`: Mengumpulkan event keyboard/mouse dari antrian OS.
  2. `update(dt)`: Memperbarui posisi koordinat, timer, state logika, dan deteksi collision.
  3. `render(screen)`: Menggambar ulang background, sprites, dan layer HUD.

## 2. State Management (Finite State Machine - FSM)
- State disimpan dan dikontrol oleh `StateManager` / `SceneManager`.
- **Daftar State:**
  - `MENU_STATE`: Menampilkan menu utama dan mendengarkan navigasi pilihan.
  - `PLAY_STATE`: Menjalankan update fisika, collision, dan pergerakan entitas aktif.
  - `PAUSE_STATE`: Membekukan update dunia game (freeze time), merender overlay semi-transparan.
  - `END_STATE`: Menampilkan ringkasan hasil menang/kalah dan opsi retry.

## 3. Desain Berorientasi Objek (OOP)
- Kelas Induk Dasar: `pygame.sprite.Sprite` atau `Entity(Transform, Collider)`.
- Pewarisan Entitas:
  - `Player(Entity)`
  - `Enemy(Entity)` $\to$ `Minion`, `Boss`
  - `Projectile(Entity)`
- Pemisahan Modul:
  - Logika murni tidak boleh terikat langsung ke drawing pygame agar dapat diuji melalui Pytest.
