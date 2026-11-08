# Spesifikasi Health, Pertahanan & Ketahanan Pasukan (health.md)

Dokumen ini mendefinisikan sistem poin ketahanan (*Hit Points / HP*), kondisi status unit, aturan pengurangan HP, mitigasi kerusakan medan, dan resolusi kehancuran unit pemain pada **Paper Warfire** (Tanggung Jawab Role 2).

---

## 1. Atribut Ketahanan Pasukan Pemain (Unit Health Pool)

Berbeda dengan game action biasa di mana pemain hanya mengontrol 1 karakter ber-HP 100, dalam Paper Warfire pemain mengomandoi skuadron unit militer di mana **setiap unit memiliki health pool masing-masing**:

| Unit Pasukan Pemain | Max HP | Ambang Kritis (Low HP) | Mitigasi Armor Alami | Nilai Strategis Unit |
| :--- | :--- | :--- | :--- | :--- |
| **Pistol Unit** | 70 HP | $\le 20$ HP | $0$ (Tidak ada) | Ringan, umpan pengintai |
| **Machine Gun** | 90 HP | $\le 25$ HP | $0$ (Tidak ada) | Supresi infanteri musuh |
| **Sniper Unit** | 60 HP | $\le 15$ HP | $0$ (Rentan serangan jarak dekat) | Aset bernilai tinggi (*high priority*) |
| **Tank Unit** | 200 HP | $\le 50$ HP | $10\%$ reduksi damage langsung | Lini pertahanan utama & penyerap damage |
| **Mortar Unit** | 100 HP | $\le 30$ HP | $0$ (Tidak ada) | Pendukung tembakan area |
| **Artillery Unit**| 120 HP | $\le 35$ HP | $0$ (Tidak ada) | Aset serangan jarak jauh terjauh |

---

## 2. Mekanisme Penerimaan Kerusakan & Mitigasi Terrain

Ketika tembakan atau serangan artileri musuh jatuh pada tile yang ditempati oleh unit pemain pada saat **War Phase**:

$$\text{Damage Diterima} = \text{Enemy Attack Damage} \times \text{Terrain Cover Multiplier} \times (1 - \text{Armor Natural})$$

### Aturan Mitigasi Terrain (Cover System):
1. **Open Ground / Rumput:** Tidak memberikan perlindungan sama sekali ($\times 1.0$).
2. **Forest / Hutan:** Pepohonan mereduksi $20\%$ kerusakan akibat tembakan langsung proyektil ($\times 0.8$).
3. **Rocky / Benteng Bebatuan:** Bebatuan kokoh mereduksi $40\%$ kerusakan tembakan langsung ($\times 0.6$).
4. **Swamp / Rawa:** Unit terhambat di lumpur lebih rentan terhadap serangan AoE, menerima penalti $+20\%$ kerusakan ($\times 1.2$).

---

## 3. Logika Kehancuran Unit & Sinyal Permainan (Unit Destruction Lifecycle)

1. **Pengecekan HP (Zero HP Check):**
   ```python
   def apply_damage(self, damage_amount: int) -> bool:
       self.current_hp = max(0, self.current_hp - damage_amount)
       self.trigger_hit_feedback() # Kedip putih, SFX ledakan
       
       if self.current_hp == 0:
           self.is_alive = False
           return True # Unit hancur
       return False
   ```
2. **Efek Kehancuran (Death Resolution):**
   - Unit yang HP-nya mencapai 0 pada War Phase langsung ditarik dari grid permainan (*removed from active battlefield*).
   - Memunculkan animasi partikel asap/puing-puing hancur (*destroyed wreckage*).
   - Memutar SFX ledakan berat.
   - Perintah unit tersebut yang belum sempat dieksekusi pada giliran tersebut otomatis dibatalkan (*nullified*).
3. **Kondisi Kalah Pemain (Defeat Check):**
   - Pada tahap akhir War Phase, sistem memeriksa jumlah unit pemain yang masih hidup:
     ```python
     alive_player_units = [u for u in player_units if u.is_alive]
     if len(alive_player_units) == 0:
         trigger_game_over(result="DEFEAT")
     ```

---

## 4. Keterbacaan Visual Health pada HUD & Grid (UX Readability)

1. **Floating Health Bar di Atas Unit:**
   - Setiap unit memiliki bar mini di atas kepalanya:
     - Hijau: HP $> 50\%$
     - Kuning: $25\% < \text{HP} \le 50\%$
     - Merah: HP $\le 25\%$ (Status kritis / berkedip lambat).
2. **Panel Informasi Unit Terpilih:**
   - Menampilkan teks numerik resolusi tinggi: misal `HP: 160 / 200` pada panel samping HUD.
3. **Indikator Damage Floating Text:**
   - Muncul angka merah berterbangan (misal: `-40`) di atas unit saat terkena tembakan di War Phase.
