import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import add_movie, delete_movie, add_channel, remove_channel, get_all_channels, is_admin
from keyboards.admin import get_admin_keyboard, get_cancel_keyboard

logger = logging.getLogger(__name__)
router = Router()


class AddMovieStates(StatesGroup):
    """States for adding movie"""
    code = State()
    title = State()
    description = State()
    genre = State()
    duration = State()
    video = State()


class AddChannelState(StatesGroup):
    """State for adding channel"""
    username = State()


class RemoveChannelState(StatesGroup):
    """State for removing channel"""
    username = State()


class DeleteMovieState(StatesGroup):
    """State for deleting movie"""
    code = State()


@router.message(Command('admin'))
async def cmd_admin(message: Message):
    """Show admin panel"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("❌ Sizda admin huquqi yo'q")
        return
    
    keyboard = get_admin_keyboard()
    await message.answer(
        "👨‍💼 Admin panel\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=keyboard
    )


@router.message(F.text == "➕ Kino qo'shish")
async def btn_add_movie(message: Message, state: FSMContext):
    """Button handler for add movie"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q")
        return
    
    await state.set_state(AddMovieStates.code)
    await message.answer(
        "📝 Yangi kino qo'shamiz!\n\n"
        "Qadam 1/6: Kino kodini yuboring (faqat raqamlar)",
        reply_markup=get_cancel_keyboard()
    )


@router.message(F.text == "🗑 Kino o'chirish")
async def btn_delete_movie(message: Message, state: FSMContext):
    """Button handler for delete movie"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q")
        return
    
    await state.set_state(DeleteMovieState.code)
    await message.answer(
        "🗑 Kino o'chirish\n\n"
        "Kino kodini yuboring:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(DeleteMovieState.code)
async def process_delete_movie_code(message: Message, state: FSMContext):
    """Process movie code for deletion"""
    code = message.text.strip()
    
    if not code.isdigit():
        await message.answer("❌ Kod faqat raqamlardan iborat bo'lishi kerak. Qaytadan urinib ko'ring:")
        return
    
    success = delete_movie(code)
    await state.clear()
    
    if success:
        await message.answer(
            f"✅ {code} kodli kino muvaffaqiyatli o'chirildi",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            f"❌ {code} kodli kino topilmadi",
            reply_markup=get_admin_keyboard()
        )


@router.message(F.text == "📢 Kanal qo'shish")
async def btn_add_channel(message: Message, state: FSMContext):
    """Button handler for add channel"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q")
        return
    
    await state.set_state(AddChannelState.username)
    await message.answer(
        "📢 Kanal qo'shish\n\n"
        "Kanal username ini yuboring (@ bilan yoki @ siz):",
        reply_markup=get_cancel_keyboard()
    )


@router.message(AddChannelState.username)
async def process_add_channel_username(message: Message, state: FSMContext):
    """Process channel username for adding"""
    username = message.text.strip()
    
    # Ensure username starts with @
    if not username.startswith('@'):
        username = '@' + username
    
    success = add_channel(username)
    await state.clear()
    
    if success:
        await message.answer(
            f"✅ {username} kanali muvaffaqiyatli qo'shildi",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            f"❌ {username} kanali allaqachon mavjud",
            reply_markup=get_admin_keyboard()
        )


@router.message(F.text == "❌ Kanal o'chirish")
async def btn_remove_channel(message: Message, state: FSMContext):
    """Button handler for remove channel"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q")
        return
    
    channels = get_all_channels()
    if not channels:
        await message.answer("📝 Hali kanallar qo'shilmagan", reply_markup=get_admin_keyboard())
        return
    
    channels_list = "\n".join([f"• {ch}" for ch in channels])
    await state.set_state(RemoveChannelState.username)
    await message.answer(
        f"❌ Kanal o'chirish\n\n"
        f"Qaysi kanalni o'chirmoqchisiz?\n\n{channels_list}\n\n"
        f"Kanal username ini yuboring:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(RemoveChannelState.username)
async def process_remove_channel_username(message: Message, state: FSMContext):
    """Process channel username for removal"""
    username = message.text.strip()
    
    # Ensure username starts with @
    if not username.startswith('@'):
        username = '@' + username
    
    success = remove_channel(username)
    await state.clear()
    
    if success:
        await message.answer(
            f"✅ {username} kanali muvaffaqiyatli o'chirildi",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            f"❌ {username} kanali topilmadi",
            reply_markup=get_admin_keyboard()
        )


@router.message(F.text == "📋 Kanallar ro'yxati")
async def btn_list_channels(message: Message):
    """Button handler for list channels"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q")
        return
    
    channels = get_all_channels()
    
    if not channels:
        await message.answer("📝 Hali kanallar qo'shilmagan", reply_markup=get_admin_keyboard())
        return
    
    channels_list = "\n".join([f"• {ch}" for ch in channels])
    await message.answer(
        f"📝 Majburiy kanallar ({len(channels)} ta):\n\n{channels_list}",
        reply_markup=get_admin_keyboard()
    )


@router.message(F.text == "🔍 Bot holati")
async def btn_check_bot(message: Message):
    """Button handler for check bot status"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q")
        return
    
    channels = get_all_channels()
    
    if not channels:
        await message.answer("📝 Hali kanallar qo'shilmagan", reply_markup=get_admin_keyboard())
        return
    
    result = "🔍 Bot holati:\n\n"
    
    for channel in channels:
        try:
            bot_member = await message.bot.get_chat_member(chat_id=channel, user_id=message.bot.id)
            if bot_member.status in ['administrator', 'creator']:
                result += f"✅ {channel} - Admin\n"
            else:
                result += f"❌ {channel} - Admin emas\n"
        except Exception as e:
            result += f"❌ {channel} - Xatolik: {str(e)[:50]}\n"
    
    result += f"\n💡 Bot ID: {message.bot.id}"
    await message.answer(result, reply_markup=get_admin_keyboard())


@router.message(F.text == "🆔 Mening ID")
async def btn_myid(message: Message):
    """Button handler for my ID"""
    user_id = message.from_user.id
    await message.answer(
        f"👤 Sizning ma'lumotlaringiz:\n\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"👤 Ism: {message.from_user.first_name}\n"
        f"📱 Username: @{message.from_user.username or 'yo\'q'}\n\n"
        f"💡 Admin: {'✅ Ha' if is_admin(user_id) else '❌ Yo\'q'}",
        parse_mode='HTML',
        reply_markup=get_admin_keyboard() if is_admin(user_id) else None
    )


@router.message(F.text == "📊 Statistika")
async def btn_stats(message: Message):
    """Button handler for statistics"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q")
        return
    
    # TODO: Add statistics
    await message.answer(
        "📊 Statistika:\n\n"
        "Bu funksiya hali ishlab chiqilmoqda...",
        reply_markup=get_admin_keyboard()
    )


@router.message(F.text == "❌ Bekor qilish")
async def btn_cancel(message: Message, state: FSMContext):
    """Cancel current operation"""
    await state.clear()
    
    user_id = message.from_user.id
    if is_admin(user_id):
        await message.answer(
            "❌ Bekor qilindi",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer("❌ Bekor qilindi")


@router.message(Command('add_movie'))
async def cmd_add_movie(message: Message, state: FSMContext):
    """Start adding movie process"""
    await state.set_state(AddMovieStates.code)
    await message.answer(
        "📝 Yangi kino qo'shamiz!\n\n"
        "Qadam 1/6: Kino kodini yuboring (faqat raqamlar)"
    )


@router.message(AddMovieStates.code)
async def process_code(message: Message, state: FSMContext):
    """Process movie code"""
    code = message.text.strip()
    
    if not code.isdigit():
        await message.answer("❌ Kod faqat raqamlardan iborat bo'lishi kerak. Qaytadan urinib ko'ring:")
        return
    
    await state.update_data(code=code)
    await state.set_state(AddMovieStates.title)
    await message.answer("Qadam 2/6: Kino nomini yuboring")


@router.message(AddMovieStates.title)
async def process_title(message: Message, state: FSMContext):
    """Process movie title"""
    await state.update_data(title=message.text.strip())
    await state.set_state(AddMovieStates.description)
    await message.answer("Qadam 3/6: Kino tavsifini yuboring")


@router.message(AddMovieStates.description)
async def process_description(message: Message, state: FSMContext):
    """Process movie description"""
    await state.update_data(description=message.text.strip())
    await state.set_state(AddMovieStates.genre)
    await message.answer("Qadam 4/6: Kino janrini yuboring")


@router.message(AddMovieStates.genre)
async def process_genre(message: Message, state: FSMContext):
    """Process movie genre"""
    await state.update_data(genre=message.text.strip())
    await state.set_state(AddMovieStates.duration)
    await message.answer("Qadam 5/6: Kino davomiyligini yuboring (masalan: 2s 15d)")


@router.message(AddMovieStates.duration)
async def process_duration(message: Message, state: FSMContext):
    """Process movie duration"""
    await state.update_data(duration=message.text.strip())
    await state.set_state(AddMovieStates.video)
    await message.answer(
        "Qadam 6/6: Video faylni yuboring YOKI video havolasini yuboring\n\n"
        "Eslatma: Video fayl yuborish tavsiya etiladi"
    )


@router.message(AddMovieStates.video, F.video | F.document)
async def process_video_file(message: Message, state: FSMContext):
    """Process video file or document"""
    logger.info(f"Video/Document received from user {message.from_user.id}")
    
    # Send processing message
    processing_msg = await message.answer("⏳ Kino yuklanmoqda, iltimos kuting...")
    
    data = await state.get_data()
    logger.info(f"FSM data: {data}")
    
    # Get video file_id (can be video or document)
    if message.video:
        video_file_id = message.video.file_id
        logger.info(f"Video file_id: {video_file_id}")
    elif message.document:
        video_file_id = message.document.file_id
        logger.info(f"Document file_id: {video_file_id}")
    else:
        await processing_msg.delete()
        await message.answer("❌ Video topilmadi. Qaytadan urinib ko'ring:")
        return
    
    success = add_movie(
        code=data['code'],
        title=data['title'],
        description=data['description'],
        genre=data['genre'],
        duration=data['duration'],
        video_file_id=video_file_id
    )
    
    logger.info(f"Movie add result: {success}")
    
    await state.clear()
    
    # Delete processing message
    await processing_msg.delete()
    
    if success:
        await message.answer(
            f"✅ Kino muvaffaqiyatli qo'shildi!\n\n"
            f"Kod: {data['code']}\n"
            f"Nomi: {data['title']}",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            f"❌ Kino qo'shib bo'lmadi. {data['code']} kod allaqachon mavjud.",
            reply_markup=get_admin_keyboard()
        )


@router.message(AddMovieStates.video, F.text)
async def process_video_link(message: Message, state: FSMContext):
    """Process video link"""
    data = await state.get_data()
    video_link = message.text.strip()
    
    success = add_movie(
        code=data['code'],
        title=data['title'],
        description=data['description'],
        genre=data['genre'],
        duration=data['duration'],
        video_link=video_link
    )
    
    await state.clear()
    
    if success:
        await message.answer(
            f"✅ Kino muvaffaqiyatli qo'shildi!\n\n"
            f"Kod: {data['code']}\n"
            f"Nomi: {data['title']}",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            f"❌ Kino qo'shib bo'lmadi. {data['code']} kod allaqachon mavjud.",
            reply_markup=get_admin_keyboard()
        )


@router.message(Command('delete_movie'))
async def cmd_delete_movie(message: Message):
    """Delete movie command"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "Foydalanish: /delete_movie <kod>\n\n"
            "Misol: /delete_movie 1234"
        )
        return
    
    code = args[1].strip()
    
    if not code.isdigit():
        await message.answer("❌ Kod faqat raqamlardan iborat bo'lishi kerak")
        return
    
    success = delete_movie(code)
    
    if success:
        await message.answer(f"✅ {code} kodli kino muvaffaqiyatli o'chirildi")
    else:
        await message.answer(f"❌ {code} kodli kino topilmadi")


@router.message(Command('add_channel'))
async def cmd_add_channel(message: Message):
    """Add channel command"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "Foydalanish: /add_channel <username>\n\n"
            "Misol: /add_channel @mykanalim"
        )
        return
    
    username = args[1].strip()
    
    # Ensure username starts with @
    if not username.startswith('@'):
        username = '@' + username
    
    success = add_channel(username)
    
    if success:
        await message.answer(f"✅ {username} kanali muvaffaqiyatli qo'shildi")
    else:
        await message.answer(f"❌ {username} kanali allaqachon mavjud")


@router.message(Command('remove_channel'))
async def cmd_remove_channel(message: Message):
    """Remove channel command"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "Foydalanish: /remove_channel <username>\n\n"
            "Misol: /remove_channel @mykanalim"
        )
        return
    
    username = args[1].strip()
    
    # Ensure username starts with @
    if not username.startswith('@'):
        username = '@' + username
    
    success = remove_channel(username)
    
    if success:
        await message.answer(f"✅ {username} kanali muvaffaqiyatli o'chirildi")
    else:
        await message.answer(f"❌ {username} kanali topilmadi")


@router.message(Command('list_channels'))
async def cmd_list_channels(message: Message):
    """List all channels"""
    channels = get_all_channels()
    
    if not channels:
        await message.answer("📝 Hali kanallar qo'shilmagan")
        return
    
    channels_list = "\n".join([f"• {ch}" for ch in channels])
    await message.answer(
        f"📝 Majburiy kanallar ({len(channels)} ta):\n\n{channels_list}"
    )



@router.message(Command('check_bot'))
async def cmd_check_bot(message: Message):
    """Check bot permissions in channels"""
    channels = get_all_channels()
    
    if not channels:
        await message.answer("📝 Hali kanallar qo'shilmagan")
        return
    
    result = "🔍 Bot holati:\n\n"
    
    for channel in channels:
        try:
            bot_member = await message.bot.get_chat_member(chat_id=channel, user_id=message.bot.id)
            if bot_member.status in ['administrator', 'creator']:
                result += f"✅ {channel} - Admin\n"
            else:
                result += f"❌ {channel} - Admin emas\n"
        except Exception as e:
            result += f"❌ {channel} - Xatolik: {str(e)[:50]}\n"
    
    result += f"\n💡 Bot ID: {message.bot.id}"
    await message.answer(result)


@router.message(Command('myid'))
async def cmd_myid(message: Message):
    """Show user ID"""
    await message.answer(
        f"👤 Sizning ma'lumotlaringiz:\n\n"
        f"ID: <code>{message.from_user.id}</code>\n"
        f"Ism: {message.from_user.first_name}\n"
        f"Username: @{message.from_user.username or 'yo\'q'}",
        parse_mode='HTML'
    )
