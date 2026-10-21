# Spesifikasi Tampilan HUD (hud.md)

Dokumen ini mendefinisikan arsitektur antarmuka dalam permainan (*Heads-Up Display / HUD*), tata letak elemen visual, indikator status dinamis, dan sistem umpan balik pengalaman pengguna (*UX Feedback*) untuk game *OPERATION: PHANTOM WIRE* (Tanggung Jawab: **Role 3 — UI/UX Designer, Audio/Asset Integrator & QA**).

---

## 1. Tata Letak Kanvas HUD (1280 x 720 HD)

Semua elemen HUD digambar pada layer teratas (*Top Overlay Layer*) tanpa terpengaruh pergeseran kamera (*world scrolling offset*).

```
+---------------------------------------------------------------------------------------------------+
| [HP: [████████████░░░░] 75/100]                                     [ALERT STATUS: CAUTION 08s]   |
| [NOISE: [████░░░░░░░░░] 42 dB]                                     [RADAR SENSOR: ACTIVE]        |
|                                                                                                   |
|                                                                                                   |
|                                                                                                   |
|                                          (AREA GAMEPLAY)                                          |
|                                                                                                   |
|                                                                                                   |
|                                                                                                   |
| [MISI: Susup ke Ruang Kontrol & Dapatkan Keycard-3]                   [AMMO: 2/3 TRANQ DART]      |
| [E: Interaksi / Knock | SHIFT: Lari | J: Tranq]                       [SKOR TAKTIS: 02,450 PTS]   |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Rincian Komponen HUD Taktis

### A. Health Bar & Stamina (Pojok Kiri Atas - Koordinat: `X=30, Y=25`)
- **Visual Bar:** Batang horizontal ukuran $220 \times 18\text{ piksel}$.
  - Latar belakang: Hitam transparan dengan bingkai baja putih $2\text{ px}$.
  - Warna Isi: Hijau cerah (`#00ff66`) saat $\text{HP} > 50$, Kuning peringatan (`#ffcc00`) saat $25 < \text{HP} \le 50$, dan Merah berdenyut (`#ff1133`) saat $\text{HP} \le 25$.
- **Teks Numerik:** Ditampilkan di sisi kanan batang: `75 / 100 HP`.

### B. Noise Decibel Meter (Pojok Kiri Atas - di bawah HP: `X=30, Y=52`)
- **Fungsi:** Menampilkan tingkat kebisingan aktual yang dihasilkan langkah kaki atau aksi pemain.
- **Visual Bar:** Batang horizontal ukuran $160 \times 10\text{ piksel}$ dengan warna cyan taktis (`#00f0ff`).
- **Respon Dinamis:** Batang melonjak seketika saat pemain berlari atau mengetuk dinding, lalu meluruh kembali ke nol dalam $0.4\text{ detik}$.

### C. Alert Status Indicator (Pojok Kanan Atas - Koordinat: `X=980, Y=25`)
- **Format Tampilan:** Kotak radar status fasilitas berukuran $270 \times 45\text{ piksel}$.
- **Tiga Fase Status Dinamis:**
  1. **`[STATUS: INFILTRATION]`** (Teks Hijau Neon): Kondisi aman, musuh berpatroli normal.
  2. **`[CAUTION: XXs]`** (Teks Kuning Emas): Hitungan mundur 10 detik saat musuh curiga mendengar suara atau melihat bayangan.
  3. **`[ALERT / EVASION: XXs]`** (Teks Merah Menyala + Berkedip): Sirine berbunyi, musuh mengejar dan menembak. Hitungan mundur 10 detik aktif saat pemain berhasil keluar dari garis pandang musuh untuk bersembunyi.

### D. Objective Tracker (Pojok Kiri Bawah - Koordinat: `X=30, Y=660`)
- **Teks Instruksi:** Berisi nama misi aktif dan progres terkini:
  - Fase 1: `[MISI: Temukan Keycard-3 di Brankas Sektor B]`
  - Fase 2: `[MISI: Sabotase 2 Generator Listrik (1/2 Matang)]`
  - Fase 3: `[MISI: Lumpuhkan Commander Vance & Capai Lift Evakuasi!]`
- **Feedback Transisi:** Setiap kali sub-objektif selesai, teks melompat (*scale bounce*) dan memutar SFX konfirmasi radio militer.

### E. Amunisi & Skor Taktis (Pojok Kanan Bawah - Koordinat: `X=980, Y=660`)
- **Peluru Tranq Dart:** Menampilkan 3 ikon peluru kecil penenang. Ikon yang sudah digunakan berubah menjadi siluet abu-abu redup.
- **Skor Taktis:** `SCORE: 002,450 PTS` (menggunakan format zero-padded 6 digit).

---

## 3. Sistem Umpan Balik Pengalaman Pengguna (UX Feedback & Rubrik)

Sesuai kriteria **Rubrik Penilaian UX**:
1. **Kejelasan Status Seketika (Objective & Threat Clarity):**
   - Dalam 3 detik pertama bermain, pemain langsung memahami kondisi aman/bahayanya melalui warna dominan indikator status di pojok kanan atas.
2. **Efek Retinal Saat Terkena Serangan (Damage Vignette):**
   - Saat pemain terkena peluru musuh, tepi layar menampilkan vignette merah transparan (alpha 160) yang memudar perlahan selama 0.35 detik.
3. **Efek Kejut Deteksi Alarm (Alert Stinger Cue):**
   - Ketika status berubah menjadi `ALERT`, layar bergetar (*Screen Shake* intensitas 4 piksel selama 0.15 detik) disertai pemutaran instan SFX string tajam khas *Metal Gear Alert*.
