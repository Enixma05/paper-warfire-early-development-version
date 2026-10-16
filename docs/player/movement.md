# Spesifikasi Pergerakan Pemain (movement.md)

Spesifikasi logika kendali dan fisika gerak karakter pemain (Tanggung Jawab Role 2).

---

## 1. Parameter Gerak
- `MOVE_SPEED`: [Kecepatan horizontal, misal: 250 px/detik]
- `ACCELERATION` & `FRICTION`: [Akselerasi dan gesekan untuk pergerakan halus]
- `JUMP_FORCE`: [Kekuatan lompatan jika genre platformer]

## 2. Logika Input & Respon
- Input `A` / `Left`: Menghasilkan vektor arah `x = -1`. Karakter menghadap ke kiri (`flip_x = True`).
- Input `D` / `Right`: Menghasilkan vektor arah `x = 1`. Karakter menghadap ke kanan (`flip_x = False`).
- Input `W` / `Up` & `S` / `Down`: Gerak vertikal (jika game top-down).
- Normalisasi Vektor: Jika bergerak diagonal, vektor kecepatan wajib dinormalisasi agar tidak bergerak lebih cepat secara diagonal.

## 3. Pembatasan Area (Boundary Collision)
- Pemain tidak boleh keluar dari batas jendela layar (`0 <= x <= SCREEN_WIDTH - width`).
