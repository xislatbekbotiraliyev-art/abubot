# Telegram Movie Bot

A production-ready Telegram bot for sharing movies with subscription verification, built with Aiogram v3 and designed to run 24/7 on Render's free plan.

## Features

- 🎬 Movie database with SQLite
- 🔐 Channel subscription verification
- 👨‍💼 Admin panel inside bot
- 🚀 Anti-sleep mechanism for Render free plan
- 📊 Logging enabled
- ✅ Production-ready

## Project Structure

```
telegram-movie-bot/
├── handlers/
│   ├── __init__.py
│   ├── user.py          # User interaction handlers
│   └── admin.py         # Admin commands handlers
├── database/
│   ├── __init__.py
│   └── db.py            # Database operations
├── services/
│   ├── __init__.py
│   └── subscription.py  # Subscription checking logic
├── keyboards/
│   ├── __init__.py
│   └── inline.py        # Inline keyboards
├── middlewares/
│   ├── __init__.py
│   └── admin_check.py   # Admin authorization middleware
├── main.py              # Entry point
├── requirements.txt
├── Procfile            # Render deployment config
├── .env.example
├── .gitignore
└── README.md
```

## Installation & Local Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd telegram-movie-bot
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your values:
```
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=123456789,987654321
PORT=10000
```

### 5. Run locally
```bash
python main.py
```

## User Flow

1. User sends movie code (e.g., `1234`)
2. Bot checks if movie exists
3. If exists, bot checks user subscription to all channels
4. If not subscribed:
   - Shows inline buttons to join channels
   - "Check Again" button to verify
5. If subscribed:
   - Sends movie details
   - Sends video (file_id or link)

## Admin Commands

All admin commands work inside the bot:

- `/add_movie` - Add new movie (step-by-step FSM)
- `/delete_movie <code>` - Delete movie by code
- `/add_channel @username` - Add required channel
- `/remove_channel @username` - Remove channel
- `/list_channels` - List all required channels

### Adding a Movie Example

1. Send `/add_movie`
2. Bot asks for code → send `1234`
3. Bot asks for title → send `Inception`
4. Bot asks for description → send `A mind-bending thriller`
5. Bot asks for genre → send `Sci-Fi`
6. Bot asks for duration → send `2h 28m`
7. Bot asks for video → send video file OR video link

## Deployment on Render

### Step 1: Prepare Your Repository

1. Push your code to GitHub
2. Make sure `.gitignore` excludes `.env` and `*.db` files

### Step 2: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `telegram-movie-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: `Free`

### Step 3: Add Environment Variables

In Render dashboard, add these environment variables:

- `BOT_TOKEN` = Your bot token from @BotFather
- `ADMIN_IDS` = Comma-separated admin user IDs (e.g., `123456789,987654321`)
- `PORT` = `10000` (Render will override this automatically)

### Step 4: Deploy

Click "Create Web Service" and wait for deployment.

### Step 5: Get Your Service URL

After deployment, copy your service URL (e.g., `https://telegram-movie-bot.onrender.com`)

## Anti-Sleep Setup with UptimeRobot

Render's free plan sleeps after 15 minutes of inactivity. To keep it awake:

### Step 1: Create UptimeRobot Account

1. Go to [UptimeRobot](https://uptimerobot.com/)
2. Sign up for free account

### Step 2: Add Monitor

1. Click "Add New Monitor"
2. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Telegram Movie Bot
   - **URL**: `https://your-app-name.onrender.com/ping`
   - **Monitoring Interval**: 5 minutes
3. Click "Create Monitor"

### How It Works

- UptimeRobot pings `/ping` endpoint every 5 minutes
- This keeps your Render service awake 24/7
- The bot runs continuously without sleeping

## Database Schema

### movies table
```sql
code TEXT PRIMARY KEY
title TEXT NOT NULL
description TEXT
genre TEXT
duration TEXT
video_file_id TEXT
video_link TEXT
```

### channels table
```sql
username TEXT PRIMARY KEY
```

### admins table
```sql
user_id INTEGER PRIMARY KEY
```

## Security Notes

- Never commit `.env` file
- Keep `BOT_TOKEN` secret
- Only share admin access with trusted users
- Use environment variables for sensitive data

## Troubleshooting

### Bot not responding
- Check if BOT_TOKEN is correct
- Verify bot is running on Render
- Check Render logs for errors

### Subscription check not working
- Ensure bot is admin in channels
- Channel usernames must start with @
- Check bot has permission to view members

### Service sleeping on Render
- Verify UptimeRobot is pinging correctly
- Check ping interval is 5 minutes
- Ensure /ping endpoint returns "OK"

## License

MIT License - feel free to use for your projects!
