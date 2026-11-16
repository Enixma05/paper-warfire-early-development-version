# Direktori Pengujian (Tests Directory)

Direktori ini berisi seluruh kode pengujian (*automated tests*), skenario uji coba, serta laporan dan log hasil pengujian beserta pencatatan waktu testing untuk game **Paper Warfire**.

---

## 📁 Struktur Folder Pengujian

```text
tests/
├── 1st Test.txt          # Catatan mentah lapangan sesi testing pertama (User2)
├── reports/              # Arsip laporan pengujian formal, log eksekusi, dan timestamp
│   ├── TEST_LOG.md       # Laporan utama hasil testing, durasi, tanggal & waktu, serta bug tracker
│   └── test_run_*.log    # Output log pengujian otomatis dari pytest (opsional)
├── unit/                 # Unit test terisolasi per modul logic (pytest)
│   ├── test_game_loop.py # Pengujian loop & state manager (Role 1)
│   ├── test_movement.py  # Pengujian pergerakan grid & collision (Role 2)
│   ├── test_combat.py    # Pengujian kalkulasi damage & AoE (Role 2)
│   └── test_fog_of_war.py# Pengujian sistem kabut perang (Role 2)
└── README.md             # Panduan pengujian & tata cara pencatatan
```

---

## 🕒 Riwayat & Pencatatan Sesi Pengujian

Seluruh hasil pengujian manual maupun otomatis dicatat secara terstruktur pada dokumen:
👉 **[`tests/reports/TEST_LOG.md`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/tests/reports/TEST_LOG.md)**

### Status Sesi Pengujian:
- **Sesi 01 (16 November 2026, 18.00 - 19.00 WITA):**
  - **Status:** `NEEDS REVISION`
  - **Ringkasan:** 13 temuan pengujian sistem awal (termasuk 1 bug kritis crash `NameError` pada `enemy_ai.py` baris 168 dan 12 masalah input/UX/mechanics).
  - **Tindak Lanjut:** Matriks pembagian tugas perbaikan bug telah ditetapkan ke Role 1, Role 2, dan Role 3 pada tabel Bug Tracker di `TEST_LOG.md`.

---

## 🚀 Perintah Eksekusi Testing (Automated Tests)

Gunakan Python dari virtual environment `proyek-gaming`:

```powershell
# 1. Menjalankan seluruh pengujian unit
.\proyek-gaming\Scripts\python.exe -m pytest tests/ -v

# 2. Menjalankan pengujian dengan menampilkan 10 tes paling lambat (profiling waktu)
.\proyek-gaming\Scripts\python.exe -m pytest tests/ -v --durations=10

# 3. Menjalankan tes pada modul tertentu saja (misal: movement)
.\proyek-gaming\Scripts\python.exe -m pytest tests/unit/test_movement.py -v
```
