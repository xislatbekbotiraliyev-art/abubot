# Kanal Qo'shish Qo'llanmasi

## Yangi Funksiyalar ✨

Bot endi quyidagi imkoniyatlarni qo'llab-quvvatlaydi:

1. **Maxfiy kanallar** - `https://t.me/+...` formatdagi linklar
2. **Kanal nomlari** - Foydalanuvchilarga kanal nomi ko'rsatiladi (username emas)
3. **Avtomatik ma'lumot olish** - Bot kanal nomini avtomatik oladi

## Kanal Qo'shish Usullari

### 1. Public kanal (username bilan)

**Variant A: Username orqali**
```
/add_channel @mykanalim
```

**Variant B: Link orqali**
```
/add_channel https://t.me/mykanalim
```

### 2. Private kanal (maxfiy)

**Faqat invite link orqali:**
```
/add_channel https://t.me/+AbCdEfGhIjKlMnO
```

## Muhim Shartlar ⚠️

1. **Bot admin bo'lishi kerak** - Kanal qo'shishdan oldin botni kanalga admin qilib qo'shing
2. **Admin huquqlari** - Bot kamida "View Members" huquqiga ega bo'lishi kerak
3. **Kanal turi** - Kanal yoki Supergroup bo'lishi mumkin

## Qadamma-qadam Qo'llanma

### Public Kanal Qo'shish

1. Kanalingizga kiring
2. Kanal sozlamalariga o'ting
3. "Administrators" → "Add Admin"
4. Botni qidiring va admin qiling
5. Botga `/add_channel @kanalingiz` yuboring

### Private Kanal Qo'shish

1. Kanalingizga kiring
2. Kanal sozlamalariga o'ting
3. "Administrators" → "Add Admin"
4. Botni qidiring va admin qiling
5. "Invite Links" → Yangi link yarating yoki mavjud linkni nusxalang
6. Botga `/add_channel https://t.me/+...` yuboring

## Admin Panel Orqali

1. `/admin` buyrug'ini yuboring
2. "📢 Kanal qo'shish" tugmasini bosing
3. Kanal username yoki linkini yuboring:
   - `@mykanalim`
   - `https://t.me/mykanalim`
   - `https://t.me/+AbCdEfGhIjK`
4. Bot avtomatik kanal ma'lumotlarini oladi va saqlaydi

## Kanal Ma'lumotlarini Ko'rish

```
/list_channels
```

Bu buyruq quyidagilarni ko'rsatadi:
- 📢 Kanal nomi
- 🆔 Kanal ID
- 👤 Username (agar public bo'lsa)

## Kanal O'chirish

1. `/list_channels` orqali kanal ID ni oling
2. `/remove_channel <kanal_id>` yuboring

Yoki admin panel orqali:
1. `/admin` → "❌ Kanal o'chirish"
2. Ro'yxatdan kanal ID ni nusxalang
3. ID ni yuboring

## Bot Holatini Tekshirish

```
/check_bot
```

Bu buyruq barcha kanallarda bot admin ekanligini tekshiradi:
- ✅ Admin - Bot to'g'ri ishlaydi
- ❌ Admin emas - Botni admin qiling

## Foydalanuvchi Ko'rinishi

Foydalanuvchi kino so'raganda:

**Eski versiya:**
```
⚠️ Quyidagi kanallarga obuna bo'ling:
➕ @kanal1 ga obuna bo'lish
➕ @kanal2 ga obuna bo'lish
```

**Yangi versiya:**
```
⚠️ Quyidagi kanallarga obuna bo'ling:
➕ Kinolar Dunyosi
➕ Yangi Filmlar
```

Kanal nomlari chiroyli va tushunarli ko'rinadi! 🎉

## Xatoliklar va Yechimlar

### "Xatolik: Chat not found"
- Bot kanalga qo'shilmagan
- Yechim: Botni kanalga admin qilib qo'shing

### "Xatolik: Bot is not a member"
- Bot kanal a'zosi emas
- Yechim: Botni kanalga qo'shing

### "Xatolik: Not enough rights"
- Bot admin emas yoki huquqlari yetarli emas
- Yechim: Botga admin huquqlarini bering

### "Kanal allaqachon mavjud"
- Bu kanal avval qo'shilgan
- Yechim: `/list_channels` orqali tekshiring

## Migratsiya (Eski Versiyadan)

Agar eski versiyadan yangilayotgan bo'lsangiz:

```bash
python migrate_channels.py
```

Bu skript:
- Eski kanal ma'lumotlarini yangi formatga o'tkazadi
- Barcha mavjud kanallarni saqlaydi
- Yangi ustunlar qo'shadi

## Maslahatlar 💡

1. **Kanal nomlarini o'zgartiring** - Kanal nomini o'zgartirsangiz, bot avtomatik yangilamaydi. Kanalni o'chirib qayta qo'shing.

2. **Bir nechta kanal** - Istalgancha kanal qo'shishingiz mumkin

3. **Test qiling** - Kanal qo'shgandan keyin `/check_bot` bilan tekshiring

4. **Backup** - Muhim kanallarni yozib qo'ying

## Misol Workflow

```
# 1. Kanal yaratish
Telegram → New Channel → "Kinolar Dunyosi"

# 2. Botni admin qilish
Channel Settings → Administrators → Add Admin → @yourbot

# 3. Kanal qo'shish
/add_channel @kinolar_dunyosi

# 4. Tekshirish
/check_bot

# 5. Test
Oddiy foydalanuvchi sifatida kino kodi yuboring
```

## Qo'shimcha Ma'lumot

- Bot har safar kanal ma'lumotlarini yangilab turadi
- Private kanallar uchun faqat ID saqlanadi
- Public kanallar uchun username va ID saqlanadi
- Kanal nomi har doim ko'rsatiladi (agar mavjud bo'lsa)

---

Savollar bo'lsa, `/admin` → "🆔 Mening ID" orqali o'z ID ingizni oling va admin bilan bog'laning! 📞
