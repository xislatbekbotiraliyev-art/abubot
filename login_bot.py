import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

print("🔄 Botni qayta login qilish...")

# Get bot info (bu avtomatik login qiladi)
response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getMe')
result = response.json()

if result['ok']:
    print("✅ Bot muvaffaqiyatly login qildi!")
    print(f"Bot nomi: {result['result']['first_name']}")
    print(f"Username: @{result['result']['username']}")
    print(f"Bot ID: {result['result']['id']}")
else:
    print("❌ Xatolik:", result)
