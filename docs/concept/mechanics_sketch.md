# Sketsa Mekanik & Aturan Bermain (Mechanics Sketch)

Dokumen ini adalah kanvas untuk merancang aksi pemain, musuh, lingkungan, dan syarat kemenangan/kekalahan sebelum diformalkan ke dalam dokumen UTS.

---

## 1. Skema Kontrol (Player Controls)
| Input / Tombol | Aksi Pemain | Keterangan / Feedback |
| :--- | :--- | :--- |
| **W / Up / Space** | Bergerak Maju / Lompat | ... |
| **A - D / Left - Right** | Bergerak Kiri - Kanan | ... |
| **J / Mouse Left** | Serangan Utama | SFX tebasan/tembakan + Screen flash kecil |
| **K / Shift** | Dash / Skill Khusus | Cooldown 2 detik |
| **Escape / P** | Pause Game | Membuka menu jeda |

---

## 2. Aksi & Kemampuan Utama (Core Mechanics)
- **Sistem Gerak:** (contoh: *Kecepatan lari konstan, ada akselerasi/dekselerasi, sistem gravitasi untuk platformer*)
- **Sistem Tempur (Combat/Interaksi):** (contoh: *Melee attack radius kecil, ranged bullet dengan proyektil berkecepatan tertentu*)
- **Resource Pemain:**
  - Health: Maksimal [100] HP
  - Stamina / Mana / Ammo (jika ada): ...

---

## 3. Jenis Rintangan & Musuh (Enemy Archetypes)
1. **Musuh Tipe 1 (Dasar/Minion):**
   - Perilaku: (contoh: *Patroli bolak-balik / mengejar lurus ke pemain jika berada dalam jarak pandang*)
   - HP & Serangan: HP [50], Damage [10]
2. **Musuh Tipe 2 (Jarak Jauh / Cepat):**
   - Perilaku: ...
   - HP & Serangan: ...
3. **Boss / Musuh Utama:**
   - Pola Serangan: (Fase 1, Fase 2)
   - HP & Serangan: HP [500]

---

## 4. Syarat Menang & Kalah (Win / Lose Conditions)
*Sesuai panduan rubrik UTS, jelaskan aturan penyelesaian secara kuantitatif:*
- **Syarat Menang (Victory):**
  - Mengalahkan target musuh sebanyak [X] musuh dan 1 Boss akhir.
  - Atau: Bertahan hidup selama [X] detik / mengumpulkan [X] item objektif.
- **Syarat Kalah (Defeat):**
  - Health pemain mencapai 0 (Game Over).
  - Atau: Waktu habis sebelum objektif selesai.

---

## 5. Item & Power-ups (Opsional)
| Nama Item | Efek | Cara Memperoleh |
| :--- | :--- | :--- |
| Medkit / Potion | Memulihkan 25 HP | Drop dari musuh atau tersebar di map |
| Special Key / Ammo | Syarat membuka pintu / melukai Boss | Drop dari musuh elit |
