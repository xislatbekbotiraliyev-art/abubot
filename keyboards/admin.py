from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    """Admin panel keyboard"""
    keyboard = [
        [
            KeyboardButton(text="➕ Kino qo'shish"),
            KeyboardButton(text="🗑 Kino o'chirish")
        ],
        [
            KeyboardButton(text="📢 Kanal qo'shish"),
            KeyboardButton(text="❌ Kanal o'chirish")
        ],
        [
            KeyboardButton(text="📋 Kanallar ro'yxati"),
            KeyboardButton(text="🔍 Bot holati")
        ],
        [
            KeyboardButton(text="🆔 Mening ID"),
            KeyboardButton(text="📊 Statistika")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Admin buyrug'ini tanlang..."
    )


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Cancel keyboard for FSM"""
    keyboard = [[KeyboardButton(text="❌ Bekor qilish")]]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
