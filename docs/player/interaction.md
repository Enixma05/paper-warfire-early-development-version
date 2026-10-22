# Spesifikasi Interaksi, Serangan & Pengintaian Pemain (interaction.md)

Dokumen ini mendefinisikan sistem interaksi kontrol, mekanisme penargetan koordinat serangan (*Coordinate-Based Targeting*), kemampuan pengintaian (*Recon / Scan*), serta transaksi pembelian upgrade pada **Paper Warfire** (Tanggung Jawab Role 2).

---

## 1. Sistem Kontrol & Seleksi Unit (Player Interaction Flow)

Interaksi pemain diatur secara terstruktur selama **Planning Phase**:

```text
[Klik Mouse Kiri pada Unit] ──► [Panel Informasi Terbuka]
                                        |
                   +--------------------+--------------------+
                   |                                         |
            [Klik Tombol MOVE]                        [Klik Tombol ATTACK]
                   |                                         |
      [Tampilkan Radius Gerak]                   [Tampilkan Jangkauan Tembak]
                   |                                         |
      [Klik Tile Tujuan Valid]                   [Input / Klik Koordinat Target]
                   |                                         |
         [Preview Ghost Marker]                   [Tampilkan Reticle Target AoE]
                   |                                         |
                   +--------------------+--------------------+
                                        |
                             [Klik CONFIRM COMMAND]
                                        |
                       [Perintah Masuk ke Daftar Antrean]
```

### Navigasi & Kontrol Kamera:
- **Mouse Left Click:** Memilih unit, tile, atau tombol aksi di UI.
- **Mouse Scroll / WASD / Arrow Keys:** Menggeser kamera (*pan battlefield*) untuk meninjau area peta yang luas tanpa membatalkan seleksi unit.
- **Escape / P:** Membuka menu Pause (Jeda pertandingan) dengan opsi melanjutkan atau kembali ke menu utama.

---

## 2. Mekanisme Serangan Koordinat Manual (Coordinate-Based Targeting)

Paper Warfire menghadirkan keunikan di mana serangan proyektil dan artileri ditujukan ke koordinat spesifik medan perang:

1. **Format Input Koordinat:**
   - Pemain dapat memasukkan koordinat melalui kotak teks UI (misal: `X: 14, Y: 09` atau label alfanumerik `H8`), atau langsung mengklik tile pada medan perang.
2. **Validasi Jangkauan (Attack Range Validation):**
   - Sistem memverifikasi jarak antara unit penyerang dan koordinat target:
     $$\text{Distance}(\text{Unit}, \text{Target}) \le \text{unit.attack\_range}$$
   - Jika koordinat target berada di luar jangkauan:
     - Antarmuka memunculkan pesan peringatan: *"Target di luar jangkauan tembak (Maks: [X] tile)"*.
     - Tombol konfirmasi dinonaktifkan.
3. **Penargetan di Balik Kabut (Blind Firing):**
   - Pemain **diizinkan menyerang koordinat yang masih tertutup Fog of War** jika koordinat tersebut berada dalam jangkauan tembak senjata unit.
   - Ini merupakan taktik krusial untuk menebak posisi persembunyian musuh (*speculative bombardment*) sekaligus membuka area kabut di sekitar titik ledakan.

---

## 3. Interaksi Pengintaian (Recon & Scan Interaction)

Untuk mengatasi kabut perang yang tebal, pemain memiliki beberapa opsi pengintaian:
1. **Pergerakan Unit Infanteri Ringan (Pistol Unit):**
   - Menggerakkan unit maju secara otomatis memperluas area pandang (*sight radius* 4 tile di sekelilingnya) begitu War Phase dieksekusi.
2. **Kemampuan Khusus Scan Drone (Recon Ability):**
   - Pemain dapat memilih item kemampuan `SCAN` pada panel komando.
   - Memasukkan koordinat target yang dicurigai.
   - Pada giliran tersebut, area $5 \times 5$ tile di sekitar koordinat target akan terbuka sepenuhnya (*revealed*) selama 1 giliran penuh tanpa harus melepaskan tembakan berbahaya.

---

## 4. Interaksi Pembelian Upgrade (Economic Transactions)

Pada sub-fase evaluasi akhir giliran (*Turn Summary Phase*):
1. **Dompet Koin Pemain:**
   - Pemain dapat melihat saldo koin aktif yang diperoleh dari bonus giliran, eliminasi unit musuh, dan pengungkapan kabut.
2. **Katalog Upgrade:**
   - Pemain dapat mengklik unit tertentu dan memilih opsi upgrade:
     - *Penetration Shells* (120 Koin)
     - *Extended Scope* (100 Koin)
     - *High-Capacity Magazine* (90 Koin)
3. **Validasi Transaksi:**
   - Jika `Player.Coins >= Upgrade.Cost`: Koin dipotong, status unit diperbarui secara permanen untuk pertandingan tersebut, dan SFX koin sukses berbunyi.
   - Jika koin tidak cukup: Tombol berwarna abu-abu redup (*disabled*) dengan keterangan saldo kurang.
