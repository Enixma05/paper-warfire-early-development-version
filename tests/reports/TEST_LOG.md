# Log Hasil Pengujian & Waktu Testing (Test Execution Log)

Dokumen ini mencatat seluruh riwayat pelaksanaan pengujian (*test runs*), hasil evaluasi (*pass/fail/bug*), waktu pengujian (*timestamp*), serta tindak lanjut perbaikan selama pengembangan **Paper Warfire** (Tanggung Jawab **Role 3: UI/UX Designer & QA Tester**).

---

## 1. Ringkasan Riwayat Pengujian (Test Run Summary)

| No | Sesi Tes | Tanggal & Waktu Pengujian | Lingkungan & Versi | Tipe Pengujian | Total Kasus | Lolos (Pass) | Masalah / Temuan | Penguji (Tester) | Status Sesi |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `SESSION-01` | **16 November 2026**<br>18.00 - 19.00 WITA (Durasi: 60 Menit) | Early Dev / Windows (user2) | Manual Playtest & System Test | 13 | 0 (Awal) -> **13 (Pasca-Perbaikan)** | 13 Temuan (Semua telah diperbaiki & lolos 23 unit tests) | Rekan Tim (User2) & AI Dev Team | **RESOLVED & VERIFIED** |

---

## 2. Laporan Lengkap Sesi Pengujian 01 (`SESSION-01`)

> **Sumber Catatan Lapangan:** Diarsip dari [`tests/1st Test.txt`](file:///d:/Documents/Kuliahan/Tugas%20Kuliah/SEDANG%20DIKERJAKAN/GAME/Final%20Project/tests/1st%20Test.txt)

- **Nama Game:** Paper Warfire
- **Tanggal Pengujian:** 16 November 2026
- **Waktu Mulai (Start):** 18.00 WITA
- **Waktu Selesai (End):** 19.00 WITA
- **Total Durasi:** 60 Menit (1 Jam Penuh)
- **Tester / Penguji:** Rekan Tim (User2 - QA Tester)
- **Lingkungan Uji:** Windows OS, Python 3.x, Pygame 2.6.x (`main.py`)
- **Status Akhir:** Ditemukan 1 bug kritis (*Crash NameError*) dan 12 masalah mekanisme/UX yang memerlukan perbaikan sebelum rilis.

---

### A. Tabel Evaluasi Kasus Uji Sesi 01

| No | Modul Terkait | Aspek / Fitur Diuji | Langkah Aksi Pengujian | Hasil yang Diharapkan (Expected) | Hasil Sebenarnya di Lapangan (Actual) | Status | Tingkat Masalah |
|---|---|---|---|---|---|---|---|
| 1 | `src/ui/` & `src/core/` | Input Text vs Shortcut Global | Memasukkan huruf P, W, A, S, D pada kotak input koordinat | Huruf masuk ke kotak input tanpa memicu shortcut sistem | Mengetik 'P' memicu jeda game (*pause*); mengetik 'W','A','S','D' menggerakkan peta kamera | **FAIL** | High (UX Conflict) |
| 2 | `src/enemy/` & `src/core/` | Transisi ke War Phase & Eksekusi AI | Klik tombol "READY" untuk memulai War Phase | Game berpindah ke War Phase dan AI mengeksekusi tembakan otonom | **Program tiba-tiba crash/berhenti** dengan `NameError: name 'pos' is not defined` pada `enemy_ai.py` | **FAIL** | **CRITICAL (CRASH)** |
| 3 | `src/ui/` | Label & Petunjuk Koordinat | Meninjau tampilan panel input koordinat target | Terdapat label dan instruksi jelas mengenai sumbu X (kolom) dan Y (baris) | Kurang penjelasan sumbu X dan Y sehingga membingungkan arah input koordinat | **FAIL** | Medium (UX) |
| 4 | `src/game/` | Spawner Posisi Awal Musuh | Memulai pertandingan baru (*New Game*) | Unit musuh bertempat di zona awal yang teratur/seimbang (kolom 21-24) | Posisi unit musuh teracak secara acak liar di sembarang tempat | **FAIL** | Medium (Balancing) |
| 5 | `src/game/` | Dimensi Kanvas / Grid Medan Perang | Mengamati ukuran peta yang dapat dijelajahi | Area grid berukuran lega $24 \times 16$ tile sesuai spesifikasi SDD | Ukuran kanvas masih terbatas ($X \le 16$, $Y \le 16$), terasa sempit | **FAIL** | Medium (Grid Spec) |
| 6 | `src/ui/` | Visualisasi Range Serangan & AoE 3x3 | Memilih aksi ATTACK pada unit | Lingkaran jangkauan senjata (*range*) dan kotak reticle AoE 3x3 terlihat jelas | Jangkauan serangan unit dan indikator area ledakan 3x3 belum terlihat | **FAIL** | High (Feedback) |
| 7 | `src/ui/` | Inspeksi Unit Musuh (Enemy Info) | Mengklik/tap pada sprite unit musuh yang terlihat | Muncul panel detail info HP dan tipe unit musuh | Belum bisa melihat info unit musuh saat di-tap/klik | **FAIL** | Medium (UI Feature) |
| 8 | `src/game/` | Urutan Resolusi Per Giliran | Memproses giliran pertempuran simultan | Urutan eksekusi jelas dan teratur: seluruh aksi MOVE diselesaikan, lalu ATTACK | Alur urutan giliran belum tegas dan perlu diformalkan: `Move > Attack` | **NEEDS FIX** | High (Combat Rule) |
| 9 | `src/game/` | Radius Gerak Unit & Variasi Medan | Memilih aksi MOVE pada unit | Radius langkah terlihat transparan dan mempertimbangkan biaya 4 variasi terrain | Radius gerak belum jelas; jenis terrain yang muncul baru 2 (tanah dan air) | **FAIL** | Medium (Terrain Spec) |
| 10 | `src/ui/` | Countdown Timer Planning Phase | Memasuki Planning Phase | Terdapat hitung mundur waktu (countdown timer) di HUD atas | Belum ada waktu hitung mundur untuk setiap Planning Phase | **FAIL** | Medium (Feature) |
| 11 | `src/game/` | Visibilitas Fog of War saat Unit Mati | Unit kawan/lawan mati di medan perang | Area yang pernah terbuka (*explored*) tetap terbuka dan tidak tertutup kembali | **Fog of War tertutup kembali menjadi gelap pekat saat ada unit yang mati** (seharusnya kabut tidak tertutup) | **FAIL** | High (Logic Bug) |
| 12 | `src/core/` & `src/ui/` | Fase Summary & Transisi Giliran | War Phase selesai menuju giliran berikutnya | Pemain diberi waktu mengamati hasil pertempuran dan aksi input dikunci selama Summary Phase | Pemain belum dibatasi aksinya dan belum ada waktu jeda observasi sebelum giliran baru | **FAIL** | Medium (FSM Flow) |
| 13 | `src/ui/` | Umpan Balik Kerusakan (Damage Text) | Serangan mengenai target musuh | Muncul teks angka kerusakan melayang (*floating damage text*) atau notifikasi hit | Kerusakan (*damage*) yang dihasilkan saat menyerang musuh belum ditampilkan | **FAIL** | High (Combat Feedback) |

---

### B. Rincian Kesalahan Sistem / Crash Traceback (Masalah No. 2)

```text
Traceback (most recent call last):
  File "C:\Users\user2\video-game\main.py", line 31, in <module>
    main()
  File "C:\Users\user2\video-game\main.py", line 28, in main
    engine.run()
  File "C:\Users\user2\video-game\src\core\engine.py", line 84, in run
    self._process_events()
  File "C:\Users\user2\video-game\src\core\engine.py", line 109, in _process_events
    self.hud.handle_event(event)
  File "C:\Users\user2\video-game\src\ui\hud.py", line 142, in handle_event
    self.btn_ready.handle_event(event)
  File "C:\Users\user2\video-game\src\ui\hud.py", line 34, in handle_event
    self.callback()
  File "C:\Users\user2\video-game\src\ui\hud.py", line 125, in on_ready_clicked
    self.session.start_war_phase()
  File "C:\Users\user2\video-game\src\core\state_manager.py", line 98, in start_war_phase
    self.enemy_ai.plan_turn(self.current_turn)
  File "C:\Users\user2\video-game\src\enemy\enemy_ai.py", line 84, in plan_turn
    cmd = self._plan_unit_action(enemy, visible_players, claimed_destinations, current_turn)
  File "C:\Users\user2\video-game\src\enemy\enemy_ai.py", line 118, in _plan_unit_action
    bombard_cmd = self._try_blind_bombardment(unit, current_turn)
  File "C:\Users\user2\video-game\src\enemy\enemy_ai.py", line 168, in _try_blind_bombardment
    pos for uid, (pos_x, pos_y, turn) in self.memory.last_known_positions.items()
NameError: name 'pos' is not defined. Did you mean: 'pow'?
```

**Analisis Penyebab Crash:**
Pada file `src/enemy/enemy_ai.py` baris 168 di fungsi `_try_blind_bombardment`, terdapat kesalahan penulisan variabel *list comprehension*. Variabel `pos` dipanggil padahal tuple hasil unpack adalah `(pos_x, pos_y, turn)`. Perbaikan: ubah `pos` menjadi `(pos_x, pos_y)` atau gunakan variabel yang tepat.

---

## 3. Matriks Tindak Lanjut Bug & Pembagian Tugas (Bug Tracker)

Berdasarkan hasil pengujian sesi 01, tugas perbaikan dibagi kepada peran masing-masing anggota tim:

| Bug ID | Modul | Deskripsi Masalah | Severity | Penanggung Jawab | Rencana Solusi Teknis | Status |
|---|---|---|---|---|---|---|
| `BUG-001` | `src/enemy/enemy_ai.py` | Crash `NameError: name 'pos'` saat AI blind bombardment | **CRITICAL** | **Role 2** (AI Programmer) | Koreksi unpack variabel tuple `(pos_x, pos_y)` pada baris 168 | **RESOLVED** |
| `BUG-002` | `src/ui/hud.py` & `src/core/engine.py` | Input teks koordinat bentrok dengan hotkey P (pause) & WASD (kamera) | **HIGH** | **Role 1 & 3** | Kunci event handler global jika kotak input teks sedang aktif (*has_focus*) | **RESOLVED** |
| `BUG-003` | `src/game/fog_of_war.py` & `src/core/engine.py` | Kabut perang yang sudah dibuka tertutup kembali saat unit mati | **HIGH** | **Role 2 & 1** | Pertahankan status `EXPLORED` permanen; render shrouded terrain terlihat selamanya | **RESOLVED** |
| `BUG-004` | `src/game/battle_resolver.py` | Urutan perputaran giliran belum tegas Move lalu Attack | **HIGH** | **Role 1 & 2** | Pastikan seluruh antrean Move selesai dan posisi terupdate sebelum tahap Attack | **RESOLVED** |
| `BUG-005` | `src/ui/hud.py` & `src/core/engine.py` | Tidak ada visualisasi jangkauan tembak & reticle ledakan 3x3 | **HIGH** | **Role 3** (UI) | Gambar overlay lingkaran radius tembak & kotak kuning 3x3 saat targeting | **RESOLVED** |
| `BUG-006` | `src/ui/hud.py` & `src/core/engine.py` | Angka damage serangan tidak muncul saat musuh terkena hit | **HIGH** | **Role 3** (UI) | Tambahkan komponen *Floating Damage Text* animasi melayang | **RESOLVED** |
| `BUG-007` | `src/game/battlefield.py` & `src/core/engine.py` | Ukuran grid kanvas masih $16 \times 16$, perlu diperbesar ke $24 \times 16$ | **MEDIUM** | **Role 1** (Core) | Terapkan grid $24 \times 16$ dengan label sumbu A-X dan 1-16 di tepi layar | **RESOLVED** |
| `BUG-008` | `src/game/battlefield.py` & `src/core/state_manager.py` | Posisi unit musuh acak liar di seluruh peta saat game dimulai | **MEDIUM** | **Role 2** (Spawner) | Spawn deterministik teratur di zona timur (kolom 20-22) pada petak Plains | **RESOLVED** |
| `BUG-009` | `src/game/battlefield.py` & `src/core/engine.py` | Terrain baru ada tanah dan air; radius gerak tidak jelas | **MEDIUM** | **Role 2** (Terrain) | 4 jenis terrain (Plains, Forest, Mountain, Water) dengan ikon & highlight gerak jelas | **RESOLVED** |
| `BUG-010` | `src/ui/coord_input.py` & `src/ui/hud.py` | Belum ada petunjuk/label jelas untuk sumbu X dan Y koordinat | **MEDIUM** | **Role 3** (UI) | Tambahkan label format koordinat ("H8 / X,Y 1-24,1-16") serta fleksibilitas parsing | **RESOLVED** |
| `BUG-011` | `src/ui/hud.py` & `src/core/engine.py` | Belum bisa melihat statistik musuh saat di-tap/klik | **MEDIUM** | **Role 3** (UI) | Buat panel info musuh (HP bar & nama kelas) saat unit musuh terlihat diklik | **RESOLVED** |
| `BUG-012` | `src/ui/hud.py` & `src/core/state_manager.py` | Belum ada countdown timer pada Planning Phase | **MEDIUM** | **Role 3** (UI) | Tambahkan widget timer 60s hitung mundur di bar status atas HUD & auto-advance | **RESOLVED** |
| `BUG-013` | `src/core/state_manager.py` & `src/ui/hud.py` | Summary Phase belum mengunci input pemain & belum ada jeda observasi | **MEDIUM** | **Role 1** (State) | Kunci aksi tempur pada `TurnSubState.SUMMARY` dan navigasi manual via Advance button | **RESOLVED** |

---

## 4. Catatan Verifikasi & Penyelesaian Perbaikan (Post-Fix Verification)

Perbaikan kode dilakukan secara komprehensif pada **16 November 2026**:
1. **Verifikasi Unit Test Otomatis (`pytest tests/`):**
   - Seluruh 23 kasus uji unit (`tests/test_fixes_playtest1.py`, `tests/test_battle_resolver.py`, `tests/test_battlefield.py`, `tests/test_enemy_ai.py`, `tests/test_fog_of_war.py`, `tests/test_rules_and_win_conditions.py`) **100% Lolos (PASS)** tanpa kegagalan regresi.
2. **Crash Kritis (`BUG-001`):** Teratasi dengan perbaikan unpacking `(pos_x, pos_y)` di `src/enemy/enemy_ai.py`.
3. **Konflik Kontrol (`BUG-002`):** Hotkey global 'P' (pause) dan panning WASD dinonaktifkan saat input teks koordinat aktif. Tombol `Escape` mengaburkan fokus input box tanpa memicu pause.
4. **Fog of War Permanen (`BUG-003`):** Logika FoW memastikan tile `EXPLORED` tidak pernah kembali menjadi `UNEXPLORED` saat unit mati. Rendering medan perang mempertahankan visual kontur terrain yang redup (*shrouded*) selamanya.
5. **Urutan Resolusi Giliran (`BUG-004`):** Seluruh pergerakan diselesaikan terlebih dahulu (`_resolve_movement`), posisi unit diperbarui di matriks grid, kemudian serangan simultan dieksekusi (`_resolve_combat`).
6. **Visual Serangan & AoE 3x3 (`BUG-005`):** Menampilkan jangkauan tembak unit yang dipilih serta reticle ledakan 3x3 dengan status `[IN RANGE]` / `[OUT OF RANGE]`.
7. **Damage Text Feedback (`BUG-006`):** Menampilkan animasi angka kerusakan mengambang (*floating damage text*) `-XX DMG` di atas unit yang terkena serangan.
8. **Dimensi Grid & Label Sumbu (`BUG-007` & `BUG-010`):** Peta $24 \times 16$ tile dilengkapi label kolom horizontal A–X dan baris vertikal 1–16 di tepian kanvas.
9. **Spawn Musuh Terstruktur (`BUG-008`):** Formasi squad musuh ditempatkan secara deterministik di zona timur (kolom 20–22) pada petak Plains yang aman.
10. **Keragaman Medan Tempur (`BUG-009`):** 4 jenis terrain (Plains, Forest, Mountain, Water) memiliki palet warna kontras tinggi dan ikon tekstur geometris minimalis.
11. **Inspeksi Musuh (`BUG-011`):** Mengetuk unit musuh yang terlihat oleh FoW menampilkan kartu intel musuh di Unit Inspector tanpa mengaktifkan kendali unit.
12. **Countdown Timer (`BUG-012`):** Timer 60 detik aktif di Planning Phase, ditampilkan di header atas dengan peringatan warna merah saat waktu tersisa $\le 10$ detik, dan otomatis mengunci pesanan ketika waktu habis.
13. **Fase Summary Terkunci (`BUG-013`):** Tombol aksi tempur dinonaktifkan selama `TurnSubState.SUMMARY`, memberikan ruang observasi bagi pemain sebelum menekan `ADVANCE TO NEXT TURN`.
