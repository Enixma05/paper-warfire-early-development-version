# Konsep Visual, Audio & Antarmuka Pengguna (Audio-Visual & UX Canvas)

Dokumen ini adalah kanvas bagi tim (khususnya penanggung jawab UI/UX & Audio) untuk memetakan arah estetika, tata letak layar, dan daftar aset yang dibutuhkan.

---

## 1. Panduan Arah Seni Visual (Art Style)
- **Gaya Grafis:** (contoh: *Pixel Art 16-bit*, *Vector Flat 2D*, *Geometric Minimalist*)
- **Palet Warna Dominan:**
  - Background: (contoh: *Gelap / Moody #1a1a24*)
  - Player: (contoh: *Biru cerah / Kontras tinggi #00f0ff*)
  - Musuh: (contoh: *Merah peringatan #ff3366*)
  - Elemen Interaktif/Drop: (contoh: *Emas berkilau #ffd700*)
- **Keterbacaan Visual (Rubrik UX):**
  - Bagaimana memastikan pemain langsung membedakan musuh, rintangan berbahaya, dan background yang aman?

---

## 2. Layout Antarmuka Pengguna (UI Wireframe Sketch)

### A. HUD In-Game (Saat Bermain)
```
+-----------------------------------------------------------+
| [HP Bar: [████████░░] 80/100]          [Score: 01500]     |
| [Objective: Kalahkan Boss 0/1]         [Timer: 02:45]     |
|                                                           |
|                                                           |
|                         [PLAYER]                          |
|                                                           |
|                                                           |
| [P/Esc: Pause]                                            |
+-----------------------------------------------------------+
```

### B. Menu Navigasi
- **Main Menu:** Start Game, Instructions / Cara Main, Credits, Quit.
- **Pause Menu:** Resume, Restart Level, Return to Main Menu.
- **Game Over Screen:** Teks "Game Over", Skor Akhir, Tombol Retry, Tombol Menu.
- **Victory Screen:** Teks "Mission Accomplished", Statistik waktu & skor, Tombol Next/Menu.

---

## 3. Rencana Kebutuhan Aset (Asset Inventory)

### A. Sprite & Visual
- [ ] Player Character (Idle, Run, Attack, Hurt)
- [ ] Enemy 1 & Enemy 2 Sprites
- [ ] Boss Sprite
- [ ] Proyektil / Peluru
- [ ] Background Tileset / Map Background
- [ ] UI Icons (Health icon, Button box)

### B. Audio & Musik (SFX / BGM)
- [ ] BGM Main Menu (santai / atmosferik)
- [ ] BGM Gameplay (intens / penuh aksi)
- [ ] SFX Serangan Player
- [ ] SFX Musuh Terkena Hit
- [ ] SFX Player Terluka (Damage feedback)
- [ ] SFX Kemenangan & Game Over
- [ ] SFX Klik Tombol UI
