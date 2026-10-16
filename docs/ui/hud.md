# Spesifikasi Tampilan HUD (hud.md)

Spesifikasi tata letak, elemen visual heads-up display, dan keterbacaan data pemain (Tanggung Jawab Role 3).

---

## 1. Komponen Utama HUD
1. **Health Bar (Pojok Kiri Atas):**
   - Batang merah dengan latar belakang hitam berbingkai putih.
   - Panjang proporsional terhadap `player.current_health / player.max_health`.
   - Menampilkan teks numerik: `80 / 100 HP`.
2. **Score Counter (Pojok Kanan Atas):**
   - Format: `SCORE: 00250` (dengan zero-padding).
3. **Objective Tracker (Tengah / Kiri Bawah):**
   - Menampilkan teks misi saat ini, misal: `Musuh Tersisa: 4/10` atau `Kalahkan Boss!`.
4. **Instruksi Pause (Pojok Kanan Bawah):**
   - Teks kecil bantuan: `[ESC / P] Pause`.

## 2. Kriteria UX & Visual Feedback
- **Feedback Saat Terluka:** Layar berkedip merah tipis transparan (alpha vignette) selama 0.1 detik.
- **Feedback Tambah Skor:** Teks skor melompat sedikit (skala membesar sesaat) saat poin bertambah.
