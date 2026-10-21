# Spesifikasi Perilaku & AI Musuh (behavior.md)

Dokumen ini mendefinisikan arsitektur kecerdasan buatan (*Artificial Intelligence*), sistem sensori (penglihatan FOV dan pendengaran), serta *Finite State Machine* (FSM) musuh untuk game *OPERATION: PHANTOM WIRE* (Tanggung Jawab: **Role 2 — Gameplay, Mechanics & AI Programmer**).

---

## 1. Arsitektur Sensori AI (Vision & Hearing Systems)

Musuh memiliki dua sistem sensorik utama yang beroperasi setiap siklus pembaruan logika (`update`):

### A. Vision System (Kerucut Pandang & Line-of-Sight)
Setiap musuh aktif memproyeksikan kerucut penglihatan (*Field of View / FOV*) di depan arah hadapnya (`facing_angle`):
- **Parameter Kerucut Pandang:**
  - `FOV_ANGLE`: $60^\circ$ (total sudut sebaran $\pm 30^\circ$ dari sumbu arah hadap).
  - `VIEW_DISTANCE`: 220 piksel dalam kondisi pencahayaan normal.
  - `DARKNESS_PENALTY`: Jika generator daya ruangan disabotase (lampu mati), `VIEW_DISTANCE` dipotong 50% menjadi 110 piksel.
- **Logika Raycasting & Line of Sight (LOS):**
  1. Hitung jarak Euclid antara posisi musuh $(x_e, y_e)$ dan pemain $(x_p, y_p)$:
     $$d = \sqrt{(x_p - x_e)^2 + (y_p - y_e)^2}$$
     Jika $d > \text{VIEW\_DISTANCE}$, pemain diabaikan.
  2. Hitung sudut relatif terhadap arah hadap musuh:
     $$\Delta\theta = |\text{atan2}(y_p - y_e, x_p - x_e) - \text{facing\_angle}|$$
     Jika $\Delta\theta > \frac{\text{FOV\_ANGLE}}{2}$, pemain berada di luar busur penglihatan.
  3. Uji Garis Pandang (*Obstacle Raycast*): Buat segmen garis antara titik pusat musuh dan pemain. Jika garis berpotongan dengan salah satu `ObstacleCollider` (tembok, pilar, kontainer), pandangan terhalang.
- **Tingkat Respon Deteksi (Detection Gauge):**
  - **Jarak Dekat ($d \le 80\text{ px}$):** Deteksi instan. Nilai kecurigaan langsung 100%, memicu status **`ALERT`** dan membunyikan alarm.
  - **Jarak Jauh ($80\text{ px} < d \le \text{VIEW\_DISTANCE}$):** Nilai kecurigaan terisi bertahap ($150\%\text{ per detik}$). Jika pemain segera berlindung sebelum 100%, musuh hanya berganti ke status **`SUSPICIOUS / CAUTION`** untuk memeriksa lokasi terakhir pemain terlihat.

### B. Hearing System (Deteksi Getaran & Kebisingan)
- Setiap aksi pemain menghasilkan denyut suara dengan radius tertentu (`sound_radius`):
  - Berjalan biasa (*Sneak/Walk*): 30 piksel.
  - Berlari (*Sprint*): 130 piksel.
  - Mengetuk tembok (*Wall Knock*): 180 piksel (menembus celah lorong terdekat).
  - Tembakan senjata (*Unsuppressed* jika ada): 350 piksel.
- **Logika Respon Suara:**
  - Jika posisi musuh berada di dalam `sound_radius`:
    1. Musuh menghentikan rute patroli sementara.
    2. Menghadap ke arah sumber koordinat suara.
    3. Masuk ke state `INVESTIGATE` untuk bergerak perlahan menuju titik asal suara.

---

## 2. Finite State Machine (FSM) Musuh

```
               ┌────────────────────────────────────────────────────────┐
               │                                                        │
               ▼                                                        │
        ┌──────────────┐      Mendengar Suara      ┌─────────────────┐  │ Waktu Caution
        │  PATROL /    │ ────────────────────────► │   INVESTIGATE   │ ─┘ Habis (Kembali
        │  WAYPOINT    │                           │   (CAUTION `?`) │    ke Patroli)
        └──────────────┘                           └─────────────────┘
               │                                            │
               │ Melihat Pemain                             │ Melihat Pemain
               ▼                                            ▼
        ┌─────────────────────────────────────────────────────────────┐
        │                        ALERT / COMBAT                       │
        │                          (Status `!`)                       │
        └─────────────────────────────────────────────────────────────┘
               │                                            ▲
               │ Menembak / Serang                          │ Musuh Mendekat
               ▼                                            │
        ┌──────────────┐                                    │
        │    ATTACK    │ ───────────────────────────────────┘
        └──────────────┘
               │
               │ HP <= 0 (Takedown / Tranq)
               ▼
        ┌──────────────┐
        │     DEAD /   │
        │ UNCONSCIOUS  │
        └──────────────┘
```

### Rincian Setiap State:
1. **`PATROL` (Status Awal / Normal):**
   - Bergerak santai dengan kecepatan `PATROL_SPEED` (60 px/dtk) menelusuri daftar koordinat waypoint: `[(x1, y1), (x2, y2), ...]`.
   - Di setiap waypoint, musuh berhenti selama 1.5 detik (`IDLE_AT_NODE`), memutar sudut pandang $90^\circ$ ke kiri dan kanan untuk memantau area.
2. **`INVESTIGATE` (Curiga / Caution Mode):**
   - Muncul tanda tanya kuning `?` mengambang di atas sprite musuh.
   - Bergerak menuju koordinat sumber gangguan suara / siluet dengan kecepatan sedang (85 px/dtk).
   - Melakukan inspeksi selama 3 detik. Jika tidak menemukan pemain, tanda `?` memudar dan musuh kembali ke rute `PATROL`.
3. **`ALERT` (Tempur & Pengejaran):**
   - Muncul tanda seru merah `!` disertai SFX deteksi ikonik.
   - Mengubah status global permainan menjadi `GLOBAL_ALERT = True`.
   - Berlari mengejar koordinat terkini pemain dengan `CHASE_SPEED` (140 px/dtk).
   - Menyiapkan senjata untuk masuk ke state `ATTACK`.
4. **`ATTACK` (Mengeksekusi Tembakan):**
   - Berhenti bergerak saat berada pada jarak tembak efektif ($60 \le d \le 180\text{ px}$).
   - Membidik dan melepaskan tembakan peluru setiap interval `ATTACK_COOLDOWN` (1.2 detik).
5. **`UNCONSCIOUS / DEAD` (Tersingkir):**
   - Dipicu jika menerima *Chokehold CQC*, peluru penenang (*Tranq Dart*), atau HP habis.
   - Tubuh musuh rebah ke lantai (`is_active = False`), kerucut pandang dinonaktifkan.
   - Jika ada musuh lain yang berpatroli dan melihat tubuh rekannya yang tergeletak, musuh tersebut langsung membunyikan alarm fasilitas (*Alert Phase*).

---

## 3. Tipe Musuh Khusus (Enemy Archetypes)

### A. Patrol Guard (Penjaga Standar)
- **Tugas:** Menjaga koridor dan ruangan penghubung.
- **Perilaku:** Mengikuti 2-4 titik waypoint, membawa senter pandang biasa.
- **Kelemahan:** Sangat rentan dialihkan fokusnya menggunakan ketukan dinding atau lemparan koin dari arah belakang.

### B. Heavy Enforcer (Penjaga Berat / Pintu Utama)
- **Tugas:** Berdiri statis menjaga pintu akses ber-Keycard.
- **Perilaku:** Membawa perisai balistik depan yang memantulkan tembakan frontal. Kerucut pandang lebih sempit ($45^\circ$) namun jangkauan lebih jauh (260 px).
- **Kelemahan:** Hanya bisa dilumpuhkan dari sudut buta belakang (*rear stealth takedown*).

### C. Surveillance CCTV Camera (Sensor Statis)
- **Tugas:** Sensor keamanan dinding yang berputar secara otomatis.
- **Perilaku:** Sudut sapuan $90^\circ$ bolak-balik dengan siklus 4 detik. Memproyeksikan kerucut sinar hijau semi-transparan.
- **Respon:** Jika pemain melangkah ke dalam sinar, status alarm langsung berubah menjadi `ALERT` seketika.
- **Kelemahan:** Sinar padam total jika pemain berhasil mematikan generator sub-sektor atau menembaknya dengan panah EMP.

### D. Boss Entity: "Commander Vance" (The Warden)
- **Arena:** Ruang Kontrol Utama (*Mainframe Chamber*).
- **Perilaku Taktis (Boss AI FSM):**
  - **Fase 1 (Shield Active):** Vance dilindungi oleh *Personal Kinetic Shield* yang memancarkan medan listrik biru. Serangan tembakan dan CQC pemain tidak akan berefek. Vance terus memburu pemain sambil menembakkan senapan semi-otomatis berdaya rusak tinggi.
  - **Mekanik Sabotase:** Di arena terdapat 2 panel generator daya (Utara dan Selatan). Pemain harus menyelinap di antara pilar, memanfaatkan jeda tembakan Vance, lalu berinteraksi untuk menonaktifkan kedua generator tersebut.
  - **Fase 2 (Shield Down & Enraged):** Saat kedua generator padam, medan perisai Vance runtuh selama 20 detik. Vance menjadi rentan terhadap serangan taktis dari belakang atau tembakan proyektil. Vance akan bergerak lebih cepat dan melemparkan granat kejut ke arah cover pemain.
