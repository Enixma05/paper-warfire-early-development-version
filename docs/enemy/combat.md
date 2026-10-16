# Spesifikasi Tempur & Damage Musuh (combat.md)

Spesifikasi kalkulasi damage, deteksi benturan dengan proyektil/pemain, dan formula HP musuh.

---

## 1. Atribut Tempur Musuh
| Entitas Musuh | HP Maksimal | Contact Damage | Attack Cooldown | Kecepatan Gerak |
| :--- | :--- | :--- | :--- | :--- |
| **Minion Biasa** | 50 | 10 HP | 1.5 detik | 120 px/dtk |
| **Fast Stalker** | 30 | 15 HP | 1.0 detik | 200 px/dtk |
| **Boss Akhir** | 500 | 25 HP | 0.8 detik | 90 px/dtk |

## 2. Collision & Damage Resolver
- **Peluru Pemain vs Musuh:**
  - Saat `pygame.sprite.groupcollide(bullets, enemies)` terpicu:
    - Kurangi HP musuh sebesar `bullet.damage`.
    - Buat efek partikel percikan / flash warna putih pada sprite musuh.
    - Hancurkan peluru (`bullet.kill()`).
- **Musuh vs Karakter Pemain:**
  - Jika musuh bersentuhan dengan pemain dan pemain sedang tidak dalam status `i-frames`:
    - Panggil `player.take_damage(enemy.contact_damage)`.
    - Dorong pemain mundur sedikit (*knockback*).
