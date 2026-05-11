import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

print("🔄 Telegram bot connectionlarini tozalash...")

# 1. Delete webhook
response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true')
print("1. Delete webhook:", response.json())

time.sleep(2)

# 2. Close all connections
response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/close')
print("2. Close connections:", response.json())

time.sleep(2)

# 3. Logout
response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/logOut')
print("3. Logout:", response.json())

time.sleep(2)

# 4. Check bot info
response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getMe')
print("4. Bot info:", response.json())

print("\n✅ Barcha eski connectionlar tozalandi!")
print("⏳ 30 soniya kuting, keyin Render da botni qayta deploy qiling.")

