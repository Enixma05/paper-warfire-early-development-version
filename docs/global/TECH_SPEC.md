# Technical Specification: Paper Warfire (TECH_SPEC.md)

Dokumen arsitektur teknis perangkat lunak, siklus hidup Game Loop, Finite State Machine (FSM), serta desain kelas berorientasi objek (OOP) untuk **Paper Warfire** (Tanggung Jawab Role 1).

---

## 1. Arsitektur Game Loop & Time Management

Game menggunakan pola loop standar industri yang memisahkan pembacaan input, pembaruan logika, dan penggambaran visual:

```python
while running:
    dt = clock.tick(TARGET_FPS) / 1000.0  # Delta time dalam satuan detik
    
    # 1. Input Processing
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        state_manager.handle_event(event)
        
    # 2. Logic Update
    state_manager.update(dt)
    
    # 3. Visual Rendering
    screen.fill(COLOR_BG)
    state_manager.render(screen)
    pygame.display.flip()
```

### Parameter Waktu & Kestabilan:
- **Target FPS:** 60 FPS terkunci via `pygame.time.Clock()`.
- **Delta Time (`dt`):** Digunakan untuk interpolasi animasi pergerakan unit saat War Phase, efek kedip visual (*flashing*), dan transisi kamera, menjamin kelancaran tampilan di semua mesin PC.

---

## 2. Finite State Machine (FSM) Arsitektur Game

Transisi antar layar dan fase pertandingan dikelola secara terpusat oleh `GameStateManager`:

```text
               +-------------------+
               |    MENU_STATE     |
               +---------+---------+
                         | [Mulai Pertandingan]
                         v
               +-------------------+ <--------------------+
               |   PLAYING_STATE   |                      |
               | (Battle Manager)  |                      |
               +----+---------+----+                      |
                    |         |                           |
       [Tekan ESC]  |         | [War Phase Selesai &      |
                    v         |  Unit Habis]              |
        +---------------+     |                           |
        |  PAUSE_STATE  |     +------------+              |
        +-------+-------+                  |              |
                |                          v              |
     [Resume]   |               +--------------------+    |
     +----------+               |     END_STATE      |    |
     |                          | (Victory / Defeat) |    |
     v                          +----------+---------+    |
 [Kembali ke Gameplay]                     |              |
                                           +--------------+
                                             [Main Lagi / Retry]
```

### Sub-State Mesin Tempur di Dalam `PLAYING_STATE`:
Di dalam `PLAYING_STATE`, terdapat sub-state machine khusus untuk mengatur siklus giliran WEGO:
1. `SUB_PLANNING`: Pemain dan AI memilih aksi. Interaksi klik grid dan input koordinat aktif.
2. `SUB_WAR_EXECUTION`: Input pemain dinonaktifkan. Animasi gerakan, peluncuran peluru, ledakan, dan kalkulasi kerusakan berjalan otomatis secara berurutan.
3. `SUB_TURN_SUMMARY`: Menampilkan hasil kalkulasi giliran, perolehan koin, dan tombol menuju giliran berikutnya atau menu upgrade.

---

## 3. Struktur Kelas & Hirarki Objek (OOP Architecture)

Arsitektur kode diorganisasi secara modular per domain untuk mencegah kopling ketat (*decoupling*):

```text
src/
├── core/
│   ├── engine.py           # Game instance, loop utama, delta clock
│   ├── state_manager.py    # FSM manager global
│   └── input_handler.py    # Mouse pick, keyboard event mapper
├── game/
│   ├── battlefield.py      # Grid map data structure, tile matrix, terrain generator
│   ├── fog_of_war.py       # Bitmask visibilitas, line-of-sight & impact reveal
│   ├── battle_resolver.py  # Logika eksekusi simultan WEGO & damage calculation
│   └── command.py          # Data model perintah (MOVE, ATTACK, SCAN)
├── player/
│   ├── player_controller.py# Seleksi unit pemain, validasi perintah, upgrade wallet
│   └── player_unit.py      # Kelas turunan unit milik pemain
├── enemy/
│   ├── enemy_ai.py         # Rule-based decision maker, AI memory model
│   └── enemy_unit.py       # Kelas turunan unit milik AI
└── ui/
    ├── hud.py              # HUD atas, panel info unit, log perintah
    ├── coord_input.py      # Kotak input koordinat X/Y manual
    ├── menu.py             # Main menu, pause modal, victory/defeat screen
    └── font_manager.py     # Renderer tipografi & ikon geometri
```

### Diagram Kelas Entitas Utama (UML Hierarchy):

```text
                     +--------------------------+
                     |       Entity (Base)      |
                     +--------------------------+
                     | - grid_x, grid_y: int    |
                     | - width, height: int     |
                     | - sprite / visual_shape  |
                     +--------------------------+
                                  |
                                  v
                     +--------------------------+
                     |        BaseUnit          |
                     +--------------------------+
                     | - unit_id: str           |
                     | - unit_type: UnitType    |
                     | - team: Team (PLAYER/AI) |
                     | - max_hp, current_hp: int|
                     | - move_range: int        |
                     | - attack_range: int      |
                     | - base_damage: int       |
                     | - aoe_radius: int        |
                     | - planned_command: Command|
                     +--------------------------+
                     | + take_damage(dmg)       |
                     | + is_destroyed() -> bool |
                     +--------------------------+
                                  |
                   +--------------+--------------+
                   |                             |
                   v                             v
     +--------------------------+  +--------------------------+
     |        PlayerUnit        |  |        EnemyUnit         |
     +--------------------------+  +--------------------------+
     | + assign_command(cmd)    |  | - ai_priority_weight: int|
     | + apply_upgrade(upgrade) |  | + get_threat_score()     |
     +--------------------------+  +--------------------------+
```

---

## 4. Struktur Data Grid & Algoritma Fog of War

### Struktur Data Tile Matrix:
Medan perang disimpan sebagai matriks 2D $24 \times 16$:
```python
class Tile:
    x: int
    y: int
    terrain_type: TerrainType  # PLAINS, FOREST, MOUNTAIN, WATER
    occupant: Optional[BaseUnit]
    visibility: VisibilityState # UNEXPLORED, EXPLORED, VISIBLE
```

### Algoritma Pembaruan Kabut Perang (Line-of-Sight & Impact):
- **Distance Formula (Manhattan / Chebyshev Metric):**
  $$\text{Distance}(A, B) = \max(|A.x - B.x|, |A.y - B.y|)$$
- **Visibility Update:** Setiap awal Planning Phase dan setelah unit bergerak, semua tile dalam radius $\le \text{Sight Range}$ dari unit pemain diubah menjadi `VISIBLE`. Tile di luar radius yang pernah dilihat diturunkan menjadi `EXPLORED`.
- **Impact Reveal:** Titik serangan senjata AoE mengubah tile dalam radius $3\times 3$ menjadi `VISIBLE` sementara selama fase evaluasi.

---

## 5. Standar Testing & Kualitas Kode (QA)
- Logika hitungan murni (`BattleResolver`, `DamageCalculator`, `FogOfWar`) dirancang bebas dari dependensi modul grafis Pygame langsung, sehingga dapat diuji secara otomatis dan cepat menggunakan **`pytest tests/`**.
