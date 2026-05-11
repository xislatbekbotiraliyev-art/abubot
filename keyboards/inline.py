from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_subscription_keyboard(channels: List[Tuple[str, str, str]], movie_code: str) -> InlineKeyboardMarkup:
    """
    Create inline keyboard with channel subscription buttons
    channels: List of (channel_id, username, title) tuples
    """
    buttons = []
    
    # Add button for each channel with numbered names
    for index, channel in enumerate(channels, 1):
        channel_id, username, title = channel
        display_name = f"Kanal {index}"
        
        # Create URL for the button
        if username:
            # Public channel with username
            url = f"https://t.me/{username.lstrip('@')}"
        elif channel_id.startswith('-100'):
            # Public channel with ID (convert to link format)
            url = f"https://t.me/c/{channel_id[4:]}/1"
        else:
            # Fallback
            url = f"https://t.me/{channel_id.lstrip('@')}"
        
        buttons.append([
            InlineKeyboardButton(
                text=f"➕ {display_name}",
                url=url
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
