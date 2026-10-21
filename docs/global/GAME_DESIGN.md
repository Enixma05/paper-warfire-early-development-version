# Spesifikasi Desain Game (GAME_DESIGN.md)

Dokumen ini mendefinisikan aturan permainan mendalam, desain level, kurva kesulitan (*Difficulty Curve*), sistem penilaian taktis (*Scoring System*), dan alur naratif taktis untuk game *OPERATION: PHANTOM WIRE*.

---

## 1. Aturan Dasar & Formula Gameplay

### A. Pilar Permainan: "Stealth Action Asimetris"
- **Pemain:** Memiliki daya tahan tubuh rendah (100 HP, rentan mati dalam 3-4 tembakan) dan amunisi senjata penenang sangat terbatas (3 peluru). Kekuatan pemain terletak pada kemampuan manipulasi suara (*Wall Knock*), memanfaatkan sudut buta musuh, dan sabotase lingkungan.
- **Musuh:** Memiliki jumlah banyak, senjata otomatis mematikan, dan koordinasi alarm terpusat. Ketika musuh mendeteksi pemain, seluruh sektor fasilitas langsung meningkatkan status kewaspadaan.

### B. Rumus Desibel Suara Permukaan (Noise Decibel Formula):
Besaran radius dengar musuh dihitung dari jenis pergerakan pemain dikalikan koefisien permukaan lantai:
$$\text{Sound Radius} = \text{Base Radius} \times \text{Surface Multiplier}$$
- `Base Radius`:
  - Mengendap (*Sneak/Walk*): $30\text{ piksel}$
  - Berlari (*Sprint*): $110\text{ piksel}$
  - Mengetuk Dinding (*Wall Knock*): $180\text{ piksel}$ (mengabaikan jenis lantai)
- `Surface Multiplier`:
  - Karpet / Ruang Kontrol: $0.7\times$ (Meredam langkah kaki)
  - Lantai Beton Koridor: $1.0\times$ (Standar)
  - Kisi Logam Ventilasi / Jembatan Baja: $1.6\times$ (Sangat bising)

---

## 2. Desain Level & Kurva Progresi (Difficulty Curve)

Permainan terdiri dari 2 zona terintegrasi di dalam bunker militer *Sector-9*:

```
[Start Level] 
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│ Sektor A: Koridor Infiltrasi Barat                          │
│ • Pengenalan mekanik dasar (Sneak, Knock Dinding, CQC).    │
│ • 4 Penjaga Patroli reguler dengan rute waypoint teratur.   │
│ • 1 Kamera CCTV putar di lorong persimpangan.               │
│ • Objektif: Temukan Keycard Level-2 di ruang loker penjaga. │
└─────────────────────────────────────────────────────────────┘
      │
      ▼ (Buka Pintu Otomatis dengan Keycard-2)
┌─────────────────────────────────────────────────────────────┐
│ Sektor B: Ruang Server & Kontrol Utama                      │
│ • Kompleksitas tinggi: Ada Heavy Enforcer menjaga pintu.    │
│ • Generator Saklar Lampu untuk memotong jarak pandang musuh.│
│ • 2 Kamera CCTV terkoordinasi.                              │
│ • Objektif: Sabotase 2 Generator Daya untuk membuka ruang   │
│   Boss dan mematikan perisai kinetiknya.                    │
└─────────────────────────────────────────────────────────────┘
      │
      ▼ (Pintu Mainframe Terbuka)
┌─────────────────────────────────────────────────────────────┐
│ Sektor C: Boss Chamber (Pertarungan Commander Vance)         │
│ • Fase 1: Hindari tembakan Vance sambil mematikan generator │
│   daya di kedua sudut arena.                                │
│ • Fase 2: Perisai Vance padam, serang dari belakang untuk   │
│   melumpuhkannya.                                           │
│ • Selesai: Masuk ke lift evakuasi (Victory Screen).         │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Sistem Skor Taktis (Tactical Stealth Rating)

Di akhir misi, sistem menghitung skor akhir berdasarkan tingkat kedisiplinan stealth pemain:

| Kriteria Penilaian | Nilai Poin |
| :--- | :--- |
| **Menyelesaikan Misi (Base Clear)** | $+5000\text{ Poin}$ |
| **Ghost Takedown (CQC tanpa ketahuan)** | $+250\text{ Poin / musuh}$ |
| **Sabotase Generator Sukses** | $+500\text{ Poin / generator}$ |
| **Pemicu Alarm (Penalti Alert)** | $-1000\text{ Poin / insiden Alert}$ |
| **Membunuh Musuh Secara Kasar (Lethal Penalty)** | $-300\text{ Poin / korban}$ |
| **Bonus Kecepatan Waktu (< 4 Menit)** | $+1500\text{ Poin}$ |

### Tingkat Peringkat Akhir (Rank):
- **S-Rank (Big Boss / Phantom Master):** Skor $\ge 8000$ (0 Alarm, 100% CQC/Tranq, Cepat).
- **A-Rank (Ghost Agent):** Skor $6500 - 7999$ (Maksimal 1 kali Caution).
- **B-Rank (Operative):** Skor $4500 - 6499$ (Sempat terjadi Alert tapi berhasil lolos).
- **C-Rank (Loud Mercenary):** Skor $< 4500$ (Banyak terjadi baku tembak).
