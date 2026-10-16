# Spesifikasi Perilaku & AI Musuh (behavior.md)

Spesifikasi state machine musuh, pola patroli, dan algoritma deteksi pemain (Tanggung Jawab Role 2).

---

## 1. Tipe Musuh (Archetypes)
1. **Patrol Minion (Walker / Floater):**
   - Bergerak bolak-balik dalam batas radius tertentu atau antar titik koordinat patroli (waypoint).
   - Membalik arah saat menyentuh tembok batas.
2. **Chaser / Aggressive Enemy:**
   - Memiliki area deteksi pandangan (`DETECTION_RADIUS = 250 px`).
   - Jika jarak ke pemain `< DETECTION_RADIUS`: Ubah status menjadi `CHASE` dan dekati koordinat pemain.
3. **Boss Entity:**
   - Memiliki beberapa fase serangan (Fase 1: Tembakan berkala, Fase 2: Gerakan mengejar cepat saat HP < 50%).

## 2. State Machine Musuh (Enemy FSM)
- `IDLE`: Berdiam di tempat sementara waktu.
- `PATROL`: Bergerak mengikuti lintasan yang ditentukan.
- `CHASE`: Menghitung sudut dan bergerak mendekati posisi `player.rect.center`.
- `ATTACK`: Mengeksekusi serangan saat berada dalam jarak serang (`ATTACK_RANGE`).
- `DEAD`: Memutar animasi/partikel hancur, menjatuhkan drop item, dan memanggil `self.kill()`.
