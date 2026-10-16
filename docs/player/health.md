# Spesifikasi Health & Damage Pemain (health.md)

Spesifikasi status ketahanan, kalkulasi pengurangan HP, dan mekanisme kekebalan sementara.

---

## 1. Atribut Ketahanan
- `MAX_HEALTH`: 100 poin
- `CURRENT_HEALTH`: Dimulai dari 100 poin saat level dimulai.
- `IS_ALIVE`: Boolean flag (`True` jika `CURRENT_HEALTH > 0`, `False` jika `<= 0`).

## 2. Mekanisme Kerusakan (Take Damage)
- Fungsi: `take_damage(amount)`
- Logika: `CURRENT_HEALTH = max(0, CURRENT_HEALTH - amount)`
- Jika `CURRENT_HEALTH == 0`: Trigger event `PLAYER_DEATH` $\to$ Ganti state ke `END_STATE` (Lose).

## 3. Invulnerability Frames (i-Frames)
- Durasi: [0.8 detik] setelah terkena serangan.
- Efek Visual: Karakter berkedip (blinking effect) semi-transparan.
- Tujuan UX: Mencegah pemain langsung mati seketika terkena serangan bertubi-tubi dalam 1 frame (*damage stack spam*).
