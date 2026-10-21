# Spesifikasi Health & Damage Pemain (health.md)

Dokumen ini mendefinisikan sistem daya tahan tubuh (*Hit Points*), toleransi kerusakan asimetris, kalkulasi pengurangan HP, mekanisme perlindungan *Invulnerability Frames* (i-Frames), serta umpan balik visual saat terluka (Tanggung Jawab: **Role 2 — Gameplay, Mechanics & AI Programmer**).

---

## 1. Atribut Ketahanan & Karakteristik Fisik

| Atribut | Nilai Default | Keterangan Desain Taktis |
| :--- | :--- | :--- |
| `MAX_HEALTH` | $100\text{ HP}$ | Nilai total darah maksimum pemain. |
| `CURRENT_HEALTH` | $100\text{ HP}$ | Nilai darah saat ini (kondisi awal level selalu terisi penuh). |
| `IS_ALIVE` | `True` / `False` | Flag status hidup (`False` jika `CURRENT_HEALTH <= 0`). |
| `IFRAME_DURATION` | $0.8\text{ detik}$ | Masa kebal sementara setelah menerima satu kali serangan. |
| `REGENERATION_RATE` | $0\text{ HP/dtk}$ | Tidak ada regenerasi darah otomatis (mendorong kehati-hatian bermain stealth). |

---

## 2. Mekanisme Penerimaan Kerusakan (Damage Processing)

Pemain dirancang sangat rentan terhadap baku tembak langsung untuk menonjolkan esensi genre *Stealth Tactical*:

### A. Sumber Kerusakan & Bobot Kerusakan:
- **Peluru Penjaga Reguler (`PatrolGuard Bullet`):** $-25\text{ HP}$ (Pemain hanya mampu bertahan dari 4 tembakan).
- **Tembakan Jarak Dekat Heavy Enforcer (Shotgun Blast):** $-45\text{ HP}$ (Sangat fatal).
- **Tembakan Kaliber Berat Boss Vance:** $-35\text{ HP}$.
- **Tabrakan Fisik dengan Musuh / Knockback:** $-10\text{ HP}$.

### B. Algoritma Pengurangan Darah:
```python
def take_damage(self, amount: int, knockback_vector=(0, 0)):
    if self.is_invulnerable or not self.is_alive:
        return
    
    self.current_health = max(0, self.current_health - amount)
    
    # Menerapkan dorongan kejut mundur (knockback)
    self.apply_knockback(knockback_vector, force=180)
    
    # Mengaktifkan durasi i-Frames
    self.is_invulnerable = True
    self.iframe_timer = self.IFRAME_DURATION
    
    # Memicu event umpan balik UI/Audio
    sound_manager.play_sfx("player_hurt")
    ui_manager.trigger_damage_vignette(alpha=180)
    
    # Evaluasi kematian
    if self.current_health == 0:
        self.is_alive = False
        self.on_death()
```

---

## 3. Invulnerability Frames (i-Frames) & Umpan Balik Visual

Untuk memenuhi kriteria **Rubrik Penilaian UX (Pencegahan Frustrasi / Error Prevention)**:
- **Tujuan i-Frames:** Mencegah pemain tewas seketika dalam satu frame akibat berondongan peluru musuh yang berhimpitan (*damage stacking loop*).
- **Efek Berkedip (Blinking Sprite):**
  - Selama `iframe_timer > 0`, sprite pemain berkedip transparan dengan frekuensi $12\text{ Hz}$ (tampilan bergantian antara opacity 30% dan 100%).
- **Layar Vignette Merah (Damage Screen Flash):**
  - Permukaan layar dirender overlay merah transparan tipis yang perlahan memudar (*fade-out*) selama $0.3\text{ detik}$.

---

## 4. Mekanisme Kematian & Transisi Game Over

Ketika `CURRENT_HEALTH` mencapai angka 0:
1. **Animasi Gugur:** Karakter Agent Wraith memutar animasi jatuh ke lantai (durasi $1.2\text{ detik}$).
2. **Audio Penutup:** Memutar SFX radio statis terputus khas transmisi militer (*Signal Lost Cue*).
3. **Penghentian Logika Input:** Input keyboard langsung dinonaktifkan agar karakter tidak bisa bergerak.
4. **Pemicu Transisi State:**
   - Kirim event ke `StateManager`:
     ```python
     state_manager.switch_to("END_STATE", is_victory=False, reason="K.I.A. (Killed in Action)")
     ```
   - Menampilkan layar *Game Over* dengan opsi *Restart Sektor Ini* atau *Kembali ke Menu Utama*.
