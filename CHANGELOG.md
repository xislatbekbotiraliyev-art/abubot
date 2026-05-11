# Changelog

## [2.0.0] - 2024

### ✨ Yangi Funksiyalar

#### 📢 Maxfiy Kanallar Qo'llab-quvvatlash
- Private channel linklar qo'llab-quvvatlanadi (`https://t.me/+...`)
- Public channel linklar qo'llab-quvvatlanadi (`https://t.me/username`)
- Username orqali qo'shish (`@username`)

#### 🏷️ Kanal Nomlari
- Foydalanuvchilarga kanal nomi ko'rsatiladi (username o'rniga)
- Misol: "Kinolar Dunyosi" o'rniga "@kinolar_dunyosi" emas
- Chiroyli va tushunarli ko'rinish

#### 🗄️ Database Yangilanishi
- `channels` jadvalidagi yangi struktura:
  - `id` - Kanal ID (primary key)
  - `username` - Kanal username (agar public bo'lsa)
  - `title` - Kanal nomi (display name)

### 🔧 O'zgarishlar

#### Database (db.py)
- `add_channel()` - Endi 3 ta parametr qabul qiladi: `channel_id`, `username`, `title`
- `remove_channel()` - Endi `channel_id` orqali o'chiradi
- `get_all_channels()` - Endi tuple list qaytaradi: `(id, username, title)`

#### Admin Handler (admin.py)
- Kanal qo'shish jarayoni takomillashtirildi
- Avtomatik kanal ma'lumotlarini olish
- Link parsing qo'shildi (public va private)
- Kanal nomi bilan ko'rsatish

#### User Handler (user.py)
- FSMContext import qo'shildi
- Kanal ma'lumotlari bilan ishlash yangilandi

#### Subscription Service (subscription.py)
- Tuple list bilan ishlash
- Kanal ID orqali tekshirish

#### Inline Keyboards (inline.py)
- Kanal nomlari bilan tugmalar
- Public va private kanallar uchun to'g'ri linklar

### 📝 Yangi Fayllar

- `migrate_channels.py` - Database migratsiya skripti
- `KANAL_QOSHISH.md` - Kanal qo'shish qo'llanmasi
- `CHANGELOG.md` - O'zgarishlar tarixi

### 📚 Yangilangan Hujjatlar

- `README.md` - Yangi funksiyalar haqida ma'lumot
- Admin commands bo'limi yangilandi
- Database schema yangilandi

### 🔄 Migratsiya

Eski versiyadan yangilash uchun:
```bash
python migrate_channels.py
```

### ⚠️ Breaking Changes

- `add_channel()` funksiyasi signature o'zgardi
- `get_all_channels()` endi string list emas, tuple list qaytaradi
- Eski database strukturasi bilan ishlamaydi (migratsiya kerak)

### 🐛 Bug Fixes

- Maxfiy kanallar bilan ishlash muammosi hal qilindi
- Kanal nomi ko'rsatilmasligi muammosi hal qilindi
- Username bo'lmagan kanallar bilan ishlash yaxshilandi

### 🎯 Keyingi Versiyalar Uchun Rejalar

- [ ] Kanal statistikasi
- [ ] Kanal guruhlarini qo'llab-quvvatlash
- [ ] Kanal ma'lumotlarini avtomatik yangilash
- [ ] Kanal qo'shish uchun inline keyboard

---

## [1.0.0] - 2024

### Dastlabki Versiya

- Kino database
- Oddiy kanal subscription tekshiruvi
- Admin panel
- Render deployment
