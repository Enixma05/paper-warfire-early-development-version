# Spesifikasi Layar Akhir Game (game-over.md)

Dokumen ini mendefinisikan antarmuka dan logika transisi untuk kondisi akhir permainan (*END_STATE*), mencakup Layar Gugur Misi (*Game Over / Mission Failed Screen*) dan Layar Kemenangan Taktis (*Mission Accomplished / Victory Debriefing Screen*) (Tanggung Jawab: **Role 3 — UI/UX Designer, Audio/Asset Integrator & QA**).

---

## 1. Layar Gugur Misi (Game Over / Mission Failed)

Layar ini dipicu ketika `player.current_health <= 0` atau pemain tertangkap saat lockdown:

```
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|                                       MISSION FAILED                                              |
|                                  [ AGENT WRAITH IS K.I.A. ]                                       |
|                                                                                                   |
|                                                                                                   |
|                                    STATUS: SIGNAL LOST                                            |
|                                    WAKTU BERTAHAN : 03:14                                         |
|                                    SKOR TERCAPAI  : 01,250 PTS                                    |
|                                                                                                   |
|                                                                                                   |
|                                    [ 1. COBA LAGI (RETRY) ]                                       |
|                                    [ 2. KEMBALI KE MENU ]                                         |
|                                                                                                   |
|                                                                                                   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

### Karakteristik & Feedback Audio-Visual:
- **Warna Dominan:** Latar belakang merah darah gelap (`#1a0505`) berkedip pelan dengan efek garis statis monitor TV tabung (*CRT Scanlines*).
- **Efek Audio:** Memutar suara desis radio statis terputus (*Codec transmission lost noise*) diikuti nada minor yang dramatis.
- **Pilihan Aksi:**
  - `COBA LAGI (RETRY)`: Mengulang permainan langsung dari titik awal sektor terkini tanpa jeda loading yang lama.
  - `KEMBALI KE MENU`: Mengarahkan pemain kembali ke `MENU_STATE`.

---

## 2. Layar Kemenangan Taktis (Mission Accomplished / Victory Debriefing)

Layar ini dipicu ketika Boss *Commander Vance* berhasil dilumpuhkan dan pemain mencapai lift evakuasi akhir bunker:

```
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|                                    MISSION ACCOMPLISHED                                           |
|                               [ OPERATION: PHANTOM WIRE CLEARED ]                                 |
|                                                                                                   |
|                           -----------------------------------------                               |
|                               DATA INTI PROTOKOL : BERHASIL DIAMANKAN                             |
|                               WAKTU INFILTRASI   : 02 MENIT 48 DETIK                              |
|                               TOTAL ALARM ALERT  : 0 KALI (GHOST BONUS)                           |
|                               MUSUH DILUMPURKAN  : 5 (NON-LETHAL CQC)                             |
|                               TOTAL SKOR TAKTIS  : 08,450 PTS                                     |
|                           -----------------------------------------                               |
|                                                                                                   |
|                                   PERINGKAT TAKTIS: [ S-RANK ]                                    |
|                                    "THE PHANTOM OPERATIVE"                                        |
|                                                                                                   |
|                                     [ 1. MAIN LAGI ]                                              |
|                                     [ 2. MENU UTAMA ]                                             |
+---------------------------------------------------------------------------------------------------+
```

### Evaluasi Skor & Penentuan Peringkat (Ranking Debrief):
Rincian skor dihitung secara bertahap dengan animasi hitungan cepat (*rolling counter tally*) disertai SFX ketukan telegraf:
- **Base Clear:** $+5000\text{ Poin}$
- **Ghost Bonus (0 Alarm Alert):** $+2000\text{ Poin}$
- **Non-Lethal Bonus (100% CQC & Tranq):** $+1000\text{ Poin}$
- **Speed Bonus (< 3 Menit):** $+1500\text{ Poin}$

### Logika Tampilan Badge Peringkat:
- **S-Rank (Emas Menyala):** Skor $\ge 8000$ (Gelar: *"The Phantom Operative"*).
- **A-Rank (Perak Hijau):** Skor $6500 - 7999$ (Gelar: *"Shadow Specialist"*).
- **B-Rank (Kuning Tembaga):** Skor $4500 - 6499$ (Gelar: *"Tactical Infiltrator"*).
- **C-Rank (Abu-abu Besi):** Skor $< 4500$ (Gelar: *"Loud Mercenary"*).

### Audio Fanfare:
Memutar lagu kemenangan taktis bernuansa synthwave kemenangan (*Victory Codec Fanfare*) yang membangkitkan rasa kepuasan pemain (*Sense of Accomplishment*).
