# Spesifikasi Tempur & Damage Musuh (combat.md)

Dokumen ini merinci kalkulasi atribut numerik, tabel status musuh, sistem resolusi benturan proyektil/serangan, dan formula pertempuran (Tanggung Jawab: **Role 2 — Gameplay, Mechanics & AI Programmer**).

---

## 1. Tabel Status Kuantitatif Entitas Musuh

| Entitas | Max HP | Kecepatan Gerak (px/dtk) | Damage Serangan | Jarak Serang Efektif | Attack Cooldown | Jarak Pandang (Normal / Padam) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Patrol Guard** | 50 | 60 (Patrol) / 140 (Chase) | 15 HP | 160 px | 1.2 dtk | 220 px / 110 px |
| **Heavy Enforcer** | 120 | 40 (Guard) / 90 (Chase) | 30 HP (Shotgun) | 120 px | 2.0 dtk | 260 px / 130 px |
| **CCTV Camera** | 1 (Mekanis) | 0 (Statis berotasi) | 0 (Trigger Alarm) | 200 px | N/A | 200 px / 0 px (Padam) |
| **Boss: Vance** | 400 | 80 (Fase 1) / 130 (Fase 2) | 25 HP | 220 px | 0.9 dtk | 280 px / 180 px |

---

## 2. Sistem Tipe Serangan & Pertahanan (Combat Resolution)

Pertempuran dalam game dirancang dengan aturan asimetris: pemain memiliki daya tahan fisik rendah (3-4 kali terkena tembakan langsung kalah), sehingga stealth adalah opsi paling efektif.

### A. Serangan Pemain Terhadap Musuh:
1. **Takedown Senyap (Rear CQC Chokehold):**
   - **Kondisi:** Pemain berada di belakang musuh (selisih sudut hadap $\Delta\theta \le 45^\circ$) pada jarak sentuh ($d \le 35\text{ px}$) tanpa musuh dalam status `ALERT`.
   - **Efek:** Melumpuhkan musuh seketika dalam 1 serangan tanpa menimbulkan suara letusan senjata. Status musuh langsung berganti ke `UNCONSCIOUS`.
2. **Pistol Penenang (Silenced Tranq Dart):**
   - **Damage HP:** 0 HP (Non-letal).
   - **Efek:** Memberikan debuff `TRANQUILIZED`. Musuh akan limbung selama 0.8 detik lalu jatuh pingsan selama durasi misi.
   - **Amunisi:** Sangat terbatas (maksimal 3 dart per segmen level).
3. **Senjata Taktis / Serangan Belakang Terhadap Boss:**
   - Saat perisai Boss Vance padam, setiap serangan dari arah belakang menghasilkan $80\text{ damage}$ (20% dari total HP).

### B. Serangan Musuh Terhadap Pemain:
1. **Tembakan Proyektil Musuh (`EnemyBullet`):**
   - Kecepatan proyektil: 320 px/dtk.
   - Deteksi Benturan: Menggunakan mask / bounding box irisan `pygame.sprite.collide_mask` terhadap pemain.
   - Logika Damage:
     ```python
     if not player.is_invulnerable:
         player.take_damage(bullet.damage)
         player.trigger_iframe(duration=0.6)  # Kebal sementara 0.6 dtk
         trigger_screen_flash(color=(255, 0, 0, 80))
     bullet.kill()
     ```
2. **Kerusakan Tabrakan (Contact Damage):**
   - Jika musuh bersentuhan fisik langsung dengan pemain saat state `ALERT`, pemain menerima $10\text{ damage}$ dan terdorong mundur (*knockback*) sejauh 25 piksel berlawanan dari posisi musuh.

---

## 3. Matriks Benturan (Collision Interaction Matrix)

Tabel berikut menjadi pedoman bagi programmer dalam menyusun grup sprite dan collision solver:

| Objek Sumber $\downarrow$ \ Objek Target $\rightarrow$ | Player Body | Enemy Body | Wall / Obstacle | Generator Terminal |
| :--- | :--- | :--- | :--- | :--- |
| **Player Body** | - | Pemicu CQC (Belakang) / Terkena Contact Dmg | Terhenti (Solid Wall Collision) | Membuka Prompt Interaksi `[E]` |
| **Player Bullet (Tranq)** | Diabaikan | Melumpuhkan musuh | Peluru musnah (*spark FX*) | Diabaikan |
| **Enemy Bullet** | Mengurangi HP pemain & trigger iframe | Diabaikan (Friendly fire off) | Peluru musnah (*dust FX*) | Diabaikan |
| **Wall Knock Sound Wave** | Diabaikan | Memicu State `INVESTIGATE` | Diabaikan (Penetrasi radius) | Diabaikan |
| **Vision Raycast Line** | Memicu pengisian Detection Gauge | Diabaikan | Menghalangi pandangan (LOS Cut) | Menghalangi pandangan jika setinggi dinding |

---

## 4. Mekanisme Kematian & Pingsan (Death & Knockout Resolver)

Ketika status entitas musuh berubah menjadi pingsan / mati:
1. Panggil method `enemy.on_neutralized()`:
   - Nonaktifkan collider tempur musuh (agar tidak menghalangi pergerakan pemain di koridor sempit).
   - Matikan perhitungan FOV kerucut pandang.
   - Pindahkan sprite ke layer `GROUND_LAYER` dengan tampilan terlentang/rebah.
2. Evaluasi Skor Taktis:
   - Netralisasi tanpa terdeteksi (Ghost Takedown): $+200\text{ Skor Taktis}$.
   - Netralisasi saat alarm menyala: $+50\text{ Skor Taktis}$.
