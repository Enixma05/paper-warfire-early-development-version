# Spesifikasi Interaksi Pemain (interaction.md)

Spesifikasi benturan (collision) dan interaksi karakter dengan item, rintangan, serta proyektil.

---

## 1. Interaksi dengan Item / Pickups
- **Collision Mask:** Karakter `Player` mendeteksi overlap dengan grup sprite `PickupItems`.
- **Jenis Interaksi:**
  - Health Potion: Memanggil `player.heal(25)` hingga maksimal `MAX_HEALTH`, item di-destroy (`kill()`).
  - Score Coin: Menambahkan skor game +50 poin, memutar SFX coin.
  - Special Key / Weapon Upgrade: Mengaktifkan flag `has_boss_key = True`.

## 2. Interaksi Serangan (Attack Hitbox)
- Saat menekan tombol serang, buat hitbox sementara (`AttackHitbox`) di depan arah hadap pemain selama 0.15 detik.
- Setiap musuh yang beririsan dengan hitbox menerima damage sebesar `ATTACK_POWER`.
