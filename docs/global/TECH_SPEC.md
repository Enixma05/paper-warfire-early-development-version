# Spesifikasi Teknis & Arsitektur (TECH_SPEC.md)

Dokumen ini mendefinisikan arsitektur sistem perangkat lunak, siklus hidup eksekusi (*Main Game Loop*), *State Management* (FSM), serta struktur hirarki kelas berorientasi objek (Tanggung Jawab Utama: **Role 1 — Core Engine & Architecture / Project Leader**).

---

## 1. Arsitektur Main Game Loop & Delta Time

Game ini dibangun di atas arsitektur siklus game standar industri dengan target stabilisasi **60 Frame Per Second (FPS)** menggunakan modul `pygame.time.Clock()`.

```
                  ┌──────────────────────────────────────┐
                  ▼                                      │
          [1. Polling Event]                             │
          pygame.event.get()                             │
                  │                                      │
                  ▼                                      │
          [2. Update Logika]                             │
          current_state.update(dt)                       │
          • Integrasi Fisika & Translasi Koordinat       │  Frame Cycle
          • Raycast Penglihatan & Deteksi Benturan       │  (16.67 ms @ 60 FPS)
          • Evaluasi State Alarm & Syarat Menang/Kalah   │
                  │                                      │
                  ▼                                      │
          [3. Render Visual]                             │
          current_state.render(screen)                   │
          • Gambar Background Tiles                      │
          • Gambar Entitas (Player, Musuh, FOV, Item)    │
          • Gambar Overlay HUD & Efek Vignette Merah     │
                  │                                      │
                  ▼                                      │
          [4. Display Flip & Clock Tick] ────────────────┘
          pygame.display.flip()
          dt = clock.tick(60) / 1000.0
```

### Penerapan Delta Time (`dt`):
Seluruh kalkulasi translasi pergerakan fisik tidak menggunakan penambahan piksel konstan per frame, melainkan dikalikan variabel `dt` (dalam detik):
$$\text{posisi\_baru} = \text{posisi\_lama} + (\text{vektor\_kecepatan} \times dt)$$
*Tujuan:* Menjamin kecepatan karakter pemain dan proyektil musuh berjalan identik di komputer mana pun tanpa terpengaruh lonjakan atau penurunan frame rate.

---

## 2. Manajemen State Game (Finite State Machine / FSM)

Perpindahan alur permainan dikelola secara terpusat oleh kelas `StateManager` (atau `SceneManager`). Setiap state merupakan objek turunan dari kelas dasar abstrak `BaseState`.

```
                    ┌─────────────────┐
                    │   START APP     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
       ┌──────────► │   MENU_STATE    │
       │            └────────┬────────┘
       │                     │ Tekan "Mulai Permainan"
       │                     ▼
       │            ┌─────────────────┐       Tekan [ESC] / [P]      ┌─────────────────┐
       │            │   PLAY_STATE    │ ───────────────────────────► │   PAUSE_STATE   │
       │            │ (Stealth Game)  │ ◄─────────────────────────── │ (Freeze Update) │
       │            └────────┬────────┘         Pilih "Lanjutkan"    └────────┬────────┘
       │                     │                                                │
       │                     │ HP <= 0 (Kalah) /                              │ Pilih "Menu"
       │                     │ Boss Vance Dikalahkan (Menang)                 │
       │                     ▼                                                │
       │            ┌─────────────────┐                                       │
       └─────────── │    END_STATE    │ ◄─────────────────────────────────────┘
         Pilih      │  (Win / Lose)   │
      "Main Lagi"   └─────────────────┘
```

### Rincian Modul State:
| State | Deskripsi & Fungsi Siklus Hidup | Variabel Kunci yang Dimiliki |
| :--- | :--- | :--- |
| **`MENU_STATE`** | Layar awal pemilihan menu. Menghandle input panah/mouse untuk memilih *Start*, *How to Play*, atau *Quit*. | `selected_index`, `menu_options` |
| **`PLAY_STATE`** | Logika inti infiltrasi stealth. Mengontrol dunia game, layer tilemap, kamera scrolling, grup sprite, dan evaluasi alarm. | `player`, `enemy_group`, `alert_level`, `alarm_timer`, `objective_cleared` |
| **`PAUSE_STATE`** | Menghentikan kalkulasi pergerakan fisik (`update` dunia tidak dipanggil), merender tangkapan layar frame terakhir yang digelapkan (*semi-transparent overlay*), dan menampilkan opsi *Resume/Restart/Quit*. | `paused_surface`, `pause_options` |
| **`END_STATE`** | Menghitung skor akhir berdasarkan jumlah alarm yang terpicu, sisa waktu, dan musuh yang tersingkir. Menampilkan layar *Victory* atau *Game Over*. | `is_victory`, `final_score`, `time_elapsed` |

---

## 3. Struktur Hirarki Kelas Berorientasi Objek (OOP Architecture)

Untuk memenuhi rubrik penilaian teknis (*Object-Oriented Programming*), struktur kode disusun menggunakan konsep pewarisan (*Inheritance*) dan komposisi (*Composition*):

```
pygame.sprite.Sprite
        │
        ▼
   Entity (Kelas Induk Karakter & Objek Bergerak)
   ├── Atribut: x, y, rect, velocity, facing_angle, max_hp, current_hp
   ├── Method: move(dt), take_damage(amount), is_alive()
        │
        ├─────────────────────────────┬─────────────────────────────┐
        ▼                             ▼                             ▼
     Player                        Enemy                        Projectile
   ├── sprint_active             ├── fov_angle               ├── damage
   ├── noise_radius              ├── view_distance           ├── speed
   ├── current_ammo              ├── patrol_waypoints        └── origin_entity
   ├── do_wall_knock()           ├── enemy_fsm_state
   └── do_cqc_takedown()         ├── update_vision_raycast()
                                 └── investigate_sound()
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
                    PatrolGuard                 BossVance
                   └── senter_light            ├── shield_active
                                               ├── generator_links
                                               └── trigger_phase_two()
```

### Pemisahan Tanggung Jawab Modul (Separation of Concerns):
- `src/core/`: Berisi `engine.py`, `clock.py`, `state_manager.py`, dan `input_handler.py`. Tidak berisi logika aturan game spesifik.
- `src/player/`: Berisi kelas `Player` dan controller pergerakan.
- `src/enemy/`: Berisi kelas `Enemy`, `PatrolGuard`, `BossVance`, serta fungsi raycasting FOV.
- `src/game/`: Berisi manajemen level, generator interaktif, dan penilai kondisi menang/kalah.
- `src/ui/`: Komponen HUD, teks font rendering, dan dialog radio Codec.
