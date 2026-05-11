import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web

from database.db import init_db
from handlers import user, admin
from middlewares.admin_check import AdminCheckMiddleware

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 10000))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register middlewares LATER in main() after database init
# dp.message.middleware(AdminCheckMiddleware())

# Register handlers
# Will be registered in main() after middleware


# Web server for anti-sleep (Render compatibility)
async def handle_ping(request):
    """Health check endpoint for UptimeRobot"""
    return web.Response(text="OK")


async def start_web_server():
    """Start web server to prevent Render from sleeping"""
    app = web.Application()
    app.router.add_get('/ping', handle_ping)
    app.router.add_get('/', handle_ping)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    logger.info(f"Web server started on port {PORT}")


async def main():
    """Main function to run bot and web server"""
    # Initialize database FIRST
    init_db()
    logger.info("Database initialized")
    
    # THEN register middlewares (after database is ready)
    dp.message.middleware(AdminCheckMiddleware())
    
    # Register handlers - ADMIN FIRST!
    dp.include_router(admin.router)
    dp.include_router(user.router)
    
    # Start web server in background
    asyncio.create_task(start_web_server())
    
    # Start bot polling
    logger.info("Bot started")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
