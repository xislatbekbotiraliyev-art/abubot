from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_subscription_keyboard(channels: List[str], movie_code: str) -> InlineKeyboardMarkup:
    """Create inline keyboard with channel subscription buttons"""
    buttons = []
    
    # Add button for each channel
    for channel in channels:
        buttons.append([
            InlineKeyboardButton(
                text=f"➕ {channel} ga obuna bo'lish",
                url=f"https://t.me/{channel.lstrip('@')}"
            )
        ])
    
    # Add check again button
    buttons.append([
        InlineKeyboardButton(
            text="✅ Tekshirish",
            callback_data=f"check_sub:{movie_code}"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
