# Spesifikasi Proyek (PROJECT_SPEC.md)

Dokumen ini mendefinisikan batas cakupan, visi produk, dan tonggak capaian (*milestones*) antara **Phase 1 (UTS - Perencanaan & SDD)** dan **Phase 2 (UAS - Pengembangan, Pengujian & Revisi)** untuk game *OPERATION: PHANTOM WIRE*.

---

## 1. Identitas & Visi Proyek
- **Judul Game:** *OPERATION: PHANTOM WIRE*
- **Genre:** *2D Top-Down Tactical Stealth Action*
- **Target Platform:** Desktop PC (Windows)
- **Engine / Library:** Python 3.12 & Pygame 2.6.x (Arsitektur murni berbasis komponen OOP)
- **Inspirasi Inti:** Seri *Metal Gear* klasik (Hideo Kojima) dengan mekanisme orisinal pengukur desibel suara permukaan dan sistem sabotase generator ruangan.

---

## 2. Ruang Lingkup Proyek & Capaian (Scope & Deliverables)

### A. Phase 1: UTS — Perencanaan & Perancangan Arsitektur (Saat Ini)
Tujuan utama adalah menghasilkan cetak biru desain game yang presisi, logis, dan selaras dengan rubrik penilaian UTS:
1. **Penyusunan SDD Modular Komprehensif:**
   - Direktori `docs/concept/`: Kanvas brainstorming, rancangan mekanik, dan panduan estetika visual/audio.
   - Direktori `docs/global/`: Spesifikasi proyek, arsitektur teknis Game Loop & FSM, alur desain game, serta batasan sistem.
   - Direktori `docs/player/`, `docs/enemy/`, `docs/ui/`: Rincian fungsional modular setiap domain entitas.
2. **Sinkronisasi Dokumen Penugasan UTS (`docs/uts/Perencanaan Game.docx`):**
   - Mengisi identitas kelompok, alur Game Loop, tabel FSM State, relasi kelas OOP, serta skenario kuantitatif syarat menang/kalah.
   - Memastikan kesiapan jawaban untuk indikator Rubrik Teknis (Poin 1-5) dan Rubrik UX (Kejelasan tujuan, feedback, keterbacaan, kontrol, pencegahan frustrasi).

### B. Phase 2: UAS — Implementasi Prototipe, Testing & Revisi
Tujuan utama adalah mewujudkan gameplay fungsional yang stabil dan menyenangkan dimainkan:
1. **Core Engine:** Implementasi Game Loop 60 FPS berbasis delta time (`dt`), FSM State Manager (`MENU`, `PLAY`, `PAUSE`, `END`), dan Input Handler pusat.
2. **Stealth Gameplay & AI:**
   - Sistem pergerakan karakter pemain, ketukan dinding (*wall knock*), dan CQC Takedown.
   - AI Musuh dengan kerucut pandang raycasting, radius deteksi suara, dan eskalasi status alarm (*Normal $\to$ Caution $\to$ Alert*).
3. **Level Design & Boss Battle:**
   - Pembuatan 2 sub-sektor bunker militer (Sektor A: Infiltrasi Koridor, Sektor B: Ruang Kontrol Utama).
   - Mekanik pertarungan Boss *Commander Vance* dengan sistem perisai kinetik yang harus disabotase lewat generator.
4. **Antarmuka & Audio:** HUD dinamis (Noise Meter, HP, Alert Status), integrasi SFX langkah/alarm/tembakan, dan BGM dua lapis (*ambient sneak* vs *fast alert chase*).
5. **Quality Assurance (Pytest):** Pengujian unit test logika perhitungan damage, FSM state change, dan raycast intersection.

---

## 3. Batasan di Luar Cakupan (Out of Scope)
Untuk memastikan proyek selesai tepat waktu dan memiliki kualitas tinggi, elemen-elemen berikut berada di luar cakupan rilis ini:
- **Fitur Multiplayer / Online Networking:** Game 100% berfokus pada pengalaman taktis *Single-Player* lokal.
- **Dunia Terbuka (Open World) / Prosedural:** Seluruh peta bunker dirancang secara terstruktur (*handcrafted level design*) demi kurva kesulitan stealth yang presisi.
- **Sistem Inventaris RPG yang Kompleks:** Manajemen item dibuat ringkas (Slot Senjata Tranq Dart, Slot Keycard, dan Slot Koin Pengalih).
- **Cutscene 3D / Voice Acting Penuh:** Cerita disampaikan melalui teks transmisi Codec radio taktis 2D di awal level.
