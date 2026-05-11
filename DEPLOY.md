# GitHub va Render ga Deploy qilish

## 1. GitHub ga yuklash

### Git ni sozlash
```bash
git init
git add .
git commit -m "Initial commit: Telegram movie bot"
```

### GitHub repository yaratish
1. GitHub.com ga kiring
2. "New repository" tugmasini bosing
3. Repository nomi: `telegram-movie-bot`
4. Public yoki Private tanlang
5. "Create repository" bosing

### GitHub ga yuklash
```bash
git remote add origin https://github.com/YOUR_USERNAME/telegram-movie-bot.git
git branch -M main
git push -u origin main
```

## 2. Render ga deploy qilish

### Render account yaratish
1. https://render.com ga kiring
2. GitHub bilan ro'yxatdan o'ting

### Web Service yaratish
1. Dashboard → "New +" → "Web Service"
2. GitHub repository ni ulang
3. Sozlamalar:
   - **Name**: telegram-movie-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free

### Environment Variables qo'shish
Render dashboard da "Environment" bo'limiga:
```
BOT_TOKEN = 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_IDS = 123456789,987654321
```

### Deploy qilish
"Create Web Service" tugmasini bosing - avtomatik deploy bo'ladi!

## 3. UptimeRobot sozlash

### Account yaratish
1. https://uptimerobot.com ga kiring
2. Ro'yxatdan o'ting (bepul)

### Monitor qo'shish
1. "Add New Monitor" bosing
2. Sozlamalar:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Telegram Movie Bot
   - **URL**: https://telegram-movie-bot.onrender.com/ping
   - **Monitoring Interval**: 5 minutes
3. "Create Monitor" bosing

✅ Tayyor! Bot 24/7 ishlaydi va uxlamaydi!

## Bot tokenini olish

Agar token yo'q bo'lsa:
1. Telegram da @BotFather ni oching
2. `/newbot` yuboring
3. Bot nomini kiriting
4. Username kiriting (bot bilan tugashi kerak)
5. Token ni nusxalang

## Admin ID ni topish

1. Telegram da @userinfobot ni oching
2. `/start` yuboring
3. Sizning ID raqamingiz ko'rsatiladi
