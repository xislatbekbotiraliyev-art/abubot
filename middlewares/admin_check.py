import os
import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger(__name__)


class AdminCheckMiddleware(BaseMiddleware):
    """Middleware to check if user is admin for admin commands"""
    
    def __init__(self):
        super().__init__()
        # Get admin IDs from environment
        admin_ids_str = os.environ.get('ADMIN_IDS', '')
        
        # Debug logging
        logger.info(f"Raw ADMIN_IDS from env: '{admin_ids_str}'")
        
        if not admin_ids_str:
            logger.warning("ADMIN_IDS environment variable is empty!")
            self.admin_ids = []
        else:
            self.admin_ids = [int(id.strip()) for id in admin_ids_str.split(',') if id.strip()]
        
        logger.info(f"Loaded {len(self.admin_ids)} admin IDs: {self.admin_ids}")
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin (from environment, not database)"""
        return user_id in self.admin_ids
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Add admin check function to data
        data['is_admin'] = self.is_admin
        
        # Check if message is a command
        if event.text and event.text.startswith('/'):
            command = event.text.split()[0].lower()
            
            # Admin-only commands
            admin_commands = [
                '/add_movie', '/delete_movie',
                '/add_channel', '/remove_channel', '/list_channels',
                '/check_bot', '/admin'
            ]
            
            if command in admin_commands:
                user_id = event.from_user.id
                
                if not self.is_admin(user_id):
                    await event.answer("❌ Sizda bu buyruqdan foydalanish huquqi yo'q")
                    return
        
        return await handler(event, data)
