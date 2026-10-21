# Spesifikasi Interaksi Pemain (interaction.md)

Dokumen ini mendefinisikan seluruh aksi interaksi taktis pemain dengan lingkungan, mekanik distraksi suara dinding (*Wall Knock*), eksekusi penaklukan senyap (*CQC Rear Chokehold*), penembakan proyektil penenang (*Tranq Dart*), serta sabotase terminal generator daya (Tanggung Jawab: **Role 2 — Gameplay, Mechanics & AI Programmer**).

---

## 1. Mekanik Ketukan Dinding (Wall Knock Distraction)

Fitur orisinal warisan taktis stealth di mana pemain mengetuk permukaan dinding untuk memancing musuh mendekat:

### Alur & Logika Eksekusi:
- **Pemicu Input:** Tombol `E` atau `Space` saat karakter menempel pada dinding (jarak $\le 16\text{ piksel}$ dari `wall_collider`).
- **Kalkulasi Gelombang Suara (Pulse Sound Wave):**
  - Pemain mengeluarkan gelombang suara lingkaran dengan radius $180\text{ piksel}$ dari titik kontak dinding.
  - Memutar SFX ganda ketukan kayu/besi yang khas: *tok-tok*.
  - Render animasi cincin lingkaran kuning tipis yang mengembang keluar dari titik ketukan.
- **Respon AI Musuh:**
  - Setiap musuh di dalam radius $180\text{ piksel}$ yang sedang berstatus `PATROL` langsung beralih ke state `INVESTIGATE`.
  - Koordinat target investigasi musuh diisi dengan koordinat tepat titik ketukan dinding tersebut, bukan posisi tubuh pemain.
  - Hal ini memberi kesempatan bagi pemain untuk berputar menyusup di belakang musuh yang sedang mendekat.

---

## 2. Mekanik Penaklukan Senyap (Rear CQC Chokehold)

Aksi melumpuhkan musuh dari jarak dekat tanpa menimbulkan suara letusan senjata:

### Syarat & Verifikasi Geometri Sergap:
1. **Jarak Kontak Jarak Dekat:**
   $$d = \text{distance}(\text{player.center}, \text{enemy.center}) \le 35\text{ piksel}$$
2. **Kondisi Berada di Sudut Buta Belakang (Rear Arc):**
   - Sudut hadap pemain dan sudut hadap musuh harus searah (selisih sudut $\Delta\theta \le 45^\circ$).
3. **Status Kesiagaan Musuh:**
   - Musuh tidak sedang berada dalam status `ALERT` aktif (tidak sedang menodongkan senjata ke pemain).

### Hasil Eksekusi CQC:
- Karakter memutar animasi sergap singkat ($0.6\text{ detik}$). Selama animasi, pemain kebal dari damage minor.
- Status musuh langsung berganti ke `UNCONSCIOUS`.
- Menghasilkan $+250\text{ Skor Taktis (Ghost Takedown)}$.
- Suara takedown teredam sepenuhnya (radius suara hanya $15\text{ piksel}$).

---

## 3. Sistem Senjata Penenang (Silenced Tranq Dart Gun)

Peralatan proyektil non-letal jarak jauh beramunisi terbatas:
- **Pemicu Input:** Tombol `J` atau `Klik Kiri Mouse`.
- **Amunisi:** Maksimal $3\text{ peluru}$ per level (tidak dapat diisi ulang kecuali menemukan kotak amunisi rahasia di brankas).
- **Karakteristik Proyektil:**
  - Kecepatan Dart: $450\text{ px/detik}$.
  - Radius Suara Letusan Tembakan: $40\text{ piksel}$ (sangat senyap berkat peredam suara terintegrasi).
- **Efek Terhadap Musuh:**
  - Jika mengenai musuh reguler: Musuh limbung sesaat lalu pingsan permanen (`UNCONSCIOUS`).
  - Jika mengenai Boss Vance saat perisai aktif: Dart terpantul tanpa dampak.
  - Jika mengenai dinding: Dart hancur dan menimbulkan suara desis kecil.

---

## 4. Mekanik Sabotase Generator Daya & Terminal

Sistem interaksi lingkungan yang memicu perubahan kondisi global level:

| Objek Interaktif | Pemicu & Waktu Interaksi | Efek Gameplay yang Dihasilkan |
| :--- | :--- | :--- |
| **Generator Listrik Sub-Sektor** | Tekan & Tahan `E` selama $1.5\text{ detik}$ di dekat generator. | - Lampu sektor bunker padam total.<br>- Jarak pandang seluruh musuh di ruangan tersebut terpotong 50% (dari 220 px menjadi 110 px).<br>- Kamera CCTV di lorong padam. |
| **Komputer / Brankas Data** | Tekan `E` saat berada di dekat terminal. | - Memberikan item **Keycard Level-3**.<br>- Membuka pintu gerbang tebal menuju ruang Boss. |
| **Locker / Kotak Peti Sembunyi** | Tekan `E` di depan locker. | - Pemain masuk ke dalam locker (menjadi tak terlihat oleh raycast penglihatan musuh).<br>- Digunakan untuk menunggu alarm `ALERT` mereda menjadi `CAUTION` lalu `NORMAL`. |
