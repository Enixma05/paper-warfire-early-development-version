# Spesifikasi Pergerakan Pemain (movement.md)

Dokumen ini mendefinisikan logika kendali kontrol gerak 2D top-down, integrasi vektor fisik, sistem kecepatan ganda (*Sneak* vs *Sprint*), kalkulasi radius suara langkah, dan penanganan benturan dinding untuk karakter utama **Agent Wraith** (Tanggung Jawab: **Role 2 — Gameplay, Mechanics & AI Programmer**).

---

## 1. Parameter Fisika & Status Gerak

| Parameter | Nilai / Satuan | Keterangan & Tujuan Gameplay |
| :--- | :--- | :--- |
| `SNEAK_SPEED` (Jalan Pelan) | $90\text{ px/detik}$ | Kecepatan senyap saat mendekati musuh dari belakang. Radius suara sangat minim ($30\text{ px}$). |
| `WALK_SPEED` (Jalan Standar) | $140\text{ px/detik}$ | Kecepatan default saat menjelajahi area aman bunker ($45\text{ px}$ radius suara). |
| `SPRINT_SPEED` (Lari Cepat) | $230\text{ px/detik}$ | Dipicu saat tombol `Left Shift` ditahan. Meningkatkan kecepatan 64%, tetapi memicu radius suara bising ($110\text{ px}$ di beton, $176\text{ px}$ di kisi baja). |
| `ACCELERATION` | $1200\text{ px/detik}^2$ | Waktu akselerasi responsif ($< 0.15\text{ detik}$) menuju kecepatan puncak. |
| `FRICTION` (Pengereman) | $1500\text{ px/detik}^2$ | Pengereman instan tanpa efek licin yang mengganggu presisi manuver stealth. |
| `PLAYER_COLLIDER_SIZE` | $28 \times 28\text{ piksel}$ | Bounding box fisik di dasar kaki karakter (lebih kecil dari sprite visual $32 \times 32$ untuk kenyamanan navigasi lorong sempit). |

---

## 2. Pemrosesan Input & Normalisasi Vektor

Pengontrolan karakter mendukung keyboard (panah / tombol WASD):

```python
# Pseudo-code penanganan input vektor
move_x = 0
move_y = 0

keys = pygame.key.get_pressed()
if keys[pygame.K_w] or keys[pygame.K_UP]:    move_y -= 1
if keys[pygame.K_s] or keys[pygame.K_DOWN]:  move_y += 1
if keys[pygame.K_a] or keys[pygame.K_LEFT]:  move_x -= 1
if keys[pygame.K_d] or keys[pygame.K_RIGHT]: move_x += 1

# Normalisasi pergerakan diagonal
if move_x != 0 and move_y != 0:
    length = math.sqrt(move_x**2 + move_y**2)  # 1.414
    move_x /= length
    move_y /= length

# Penentuan arah hadap (facing_angle dalam derajat/radian)
if move_x != 0 or move_y != 0:
    self.facing_angle = math.degrees(math.atan2(move_y, move_x))
```

### Aturan Sudut Arah Hadap (Facing Angle):
- Arah hadap menentukan:
  1. Arah lemparan gadget koin distraksi.
  2. Sudut sergap penaklukan *Rear CQC Takedown*.
  3. Arah tembakan pistol penenang (*Tranq Dart*).
  4. Sisi dinding tempat karakter menempel dan mengetuk tembok (*Wall Knock*).

---

## 3. Sistem Desibel Suara Langkah Kaki (Footstep Sound Emission)

Setiap langkah karakter memancarkan denyut gelombang suara melingkar yang dapat didengar oleh AI musuh:
1. **Langkah Berulang (Footstep Interval):**
   - Berjalan: Terpicu setiap $0.45\text{ detik}$.
   - Berlari: Terpicu setiap $0.25\text{ detik}$.
2. **Kalkulasi Radius Dengar:**
   $$\text{Current Noise Radius} = \text{Base Speed Noise} \times \text{Current Floor Multiplier}$$
   - Lantai Karpet: $\text{Multiplier} = 0.7\times$
   - Lantai Beton: $\text{Multiplier} = 1.0\times$
   - Kisi Logam Ventilasi / Jembatan Baja: $\text{Multiplier} = 1.6\times$
3. **Umpan Balik Visual:**
   - Di sekitar kaki pemain muncul cincin transparan tipis (*pulse ring*) berkedip selama $0.15\text{ detik}$ yang merepresentasikan jarak jangkauan suara.
   - Indikator bar desibel di HUD (`Noise Decibel Meter`) melonjak sesuai nilai kebisingan.

---

## 4. Resolusi Benturan Dinding & Halangan (Axis-Separated Collision)

Untuk mencegah pemain "tersangkut" saat menyusuri sudut dinding, pergerakan diuji secara terpisah pada sumbu X dan sumbu Y (*Axis-Separated AABB Collision*):

1. **Update Sumbu X:**
   $$\text{posisi\_x} = \text{posisi\_x} + (v_x \times dt)$$
   - Periksa tabrakan `collider` pemain dengan `wall_colliders`.
   - Jika terjadi overlap: Geser posisi X pemain tepat ke tepi batas dinding terdekat dan setel $v_x = 0$.
2. **Update Sumbu Y:**
   $$\text{posisi\_y} = \text{posisi\_y} + (v_y \times dt)$$
   - Periksa tabrakan `collider` pemain dengan `wall_colliders`.
   - Jika terjadi overlap: Geser posisi Y pemain tepat ke tepi batas dinding terdekat dan setel $v_y = 0$.
3. **Manfaat UX:**
   - Memungkinkan pemain tetap "meluncur mulus" (*wall slide*) menyusuri tembok meskipun sedang menekan tombol arah diagonal.
