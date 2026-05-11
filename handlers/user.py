import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from database.db import get_movie, get_all_channels, is_admin
from services.subscription import check_user_subscriptions
from keyboards.inline import get_subscription_keyboard
from keyboards.admin import get_admin_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    
    # Show user ID for admin setup
    logger.info(f"User {user_id} started the bot")
    
    # Get all channels
    channels = get_all_channels()
    logger.info(f"Found {len(channels)} channels: {channels}")
    
    if channels:
        # Check subscriptions
        not_subscribed = await check_user_subscriptions(message.bot, user_id, channels)
        logger.info(f"User {user_id} not subscribed to: {not_subscribed}")
        
        if not_subscribed:
            # User not subscribed to all channels
            keyboard = get_subscription_keyboard(not_subscribed, "start")
            await message.answer(
                "⚠️ Botdan foydalanish uchun quyidagi kanallarga obuna bo'lishingiz shart:\n\n"
                "Obuna bo'lgandan so'ng 'Tekshirish' tugmasini bosing.",
                reply_markup=keyboard
            )
            return
    
    # User subscribed or no channels required
    from keyboards.admin import get_admin_keyboard
    keyboard = get_admin_keyboard() if is_admin(user_id) else None
    
    welcome_text = (
        f"👋 Kino botiga xush kelibsiz!\n\n"
        f"Kino kodini yuboring (faqat raqamlar).\n\n"
        f"Misol: 1234\n\n"
        f"<i>Sizning ID: {user_id}</i>"
    )
    
    if is_admin(user_id):
        welcome_text += "\n\n👨‍💼 Siz adminsiz! Pastdagi tugmalardan foydalaning yoki /admin buyrug'ini yuboring."
    
    await message.answer(
        welcome_text,
        parse_mode='HTML',
        reply_markup=keyboard
    )


@router.message(Command('myid'))
async def cmd_myid(message: Message):
    """Show user ID"""
    await message.answer(
        f"👤 Sizning ma'lumotlaringiz:\n\n"
        f"🆔 ID: <code>{message.from_user.id}</code>\n"
        f"👤 Ism: {message.from_user.first_name}\n"
        f"📱 Username: @{message.from_user.username or 'yo\'q'}\n\n"
        f"💡 Admin bo'lish uchun ID ni yuqorida nusxalang",
        parse_mode='HTML'
    )


@router.message(F.text.regexp(r'^\d+$'))
async def handle_movie_code(message: Message):
    """Handle movie code from user"""
    code = message.text.strip()
    user_id = message.from_user.id
    
    # Get movie from database
    movie = get_movie(code)
    
    if not movie:
        await message.answer("❌ Kino topilmadi. Kodni tekshirib qaytadan urinib ko'ring.")
        return
    
    # Unpack movie data
    movie_code, title, description, genre, duration, video_file_id, video_link = movie
    
    # Get all channels
    channels = get_all_channels()
    
    if not channels:
        # No channels to check, send movie directly
        await send_movie(message, movie)
        return
    
    # Check subscriptions
    not_subscribed = await check_user_subscriptions(message.bot, user_id, channels)
    
    if not_subscribed:
        # User not subscribed to all channels
        keyboard = get_subscription_keyboard(not_subscribed, code)
        await message.answer(
            "⚠️ Kinoni ko'rish uchun quyidagi kanallarga obuna bo'lishingiz shart:\n\n"
            "Obuna bo'lgandan so'ng 'Tekshirish' tugmasini bosing.",
            reply_markup=keyboard
        )
    else:
        # User subscribed, send movie
        await send_movie(message, movie)


@router.callback_query(F.data.startswith('check_sub:'))
async def check_subscription_callback(callback: CallbackQuery):
    """Handle check subscription callback"""
    code = callback.data.split(':')[1]
    user_id = callback.from_user.id
    
    # Get channels
    channels = get_all_channels()
    
    # Check subscriptions again
    not_subscribed = await check_user_subscriptions(callback.bot, user_id, channels)
    
    if not_subscribed:
        await callback.answer(
            "❌ Siz hali barcha kanallarga obuna bo'lmadingiz!",
            show_alert=True
        )
    else:
        # Delete the subscription message
        await callback.message.delete()
        
        # If checking from start command
        if code == "start":
            await callback.message.answer(
                "👋 Kino botiga xush kelibsiz!\n\n"
                "Kino kodini yuboring (faqat raqamlar).\n\n"
                "Misol: 1234"
            )
            await callback.answer("✅ Obuna tasdiqlandi!", show_alert=True)
        else:
            # Get movie
            movie = get_movie(code)
            if not movie:
                await callback.answer("❌ Kino topilmadi", show_alert=True)
                return
            
            # Send movie
            await send_movie(callback.message, movie)
            await callback.answer("✅ Obuna tasdiqlandi!", show_alert=True)


async def send_movie(message: Message, movie: tuple):
    """Send movie details and video to user"""
    movie_code, title, description, genre, duration, video_file_id, video_link = movie
    
    # Create beautiful caption
    caption = (
        f"🎬 <b>{title}</b>\n\n"
        f"📝 <b>Tavsif:</b> {description if description else 'Mavjud emas'}\n\n"
        f"🎭 <b>Janr:</b> {genre if genre else 'Noma\'lum'}\n"
        f"⏱ <b>Davomiyligi:</b> {duration if duration else 'Noma\'lum'}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 <b>KINO KODI:</b> <code>{movie_code}</code>"
    )
    
    # Send video with caption
    if video_file_id:
        try:
            # Try as video first
            await message.answer_video(
                video_file_id,
                caption=caption,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.info(f"Failed to send as video, trying as document: {e}")
            try:
                # If fails, try as document (.mov, .avi, etc)
                await message.answer_document(
                    video_file_id,
                    caption=caption,
                    parse_mode='HTML'
                )
            except Exception as e2:
                logger.error(f"Error sending video/document: {e2}")
                # If both fail, send details separately
                await message.answer(caption, parse_mode='HTML')
                if video_link:
                    await message.answer(f"🎥 Bu yerda tomosha qiling: {video_link}")
                else:
                    await message.answer("❌ Video yuborishda xatolik")
    elif video_link:
        await message.answer(caption, parse_mode='HTML')
        await message.answer(f"🎥 Bu yerda tomosha qiling: {video_link}")
    else:
        await message.answer(caption, parse_mode='HTML')
        await message.answer("❌ Video mavjud emas")


@router.message()
async def handle_invalid_input(message: Message, state: FSMContext):
    """Handle invalid input (only when not in FSM state)"""
    # Check if user is in FSM state
    current_state = await state.get_state()
    if current_state is not None:
        # User is in FSM state, don't handle here
        return
    
    await message.answer(
        "❌ Noto'g'ri format. Iltimos kino kodini yuboring (faqat raqamlar).\n\n"
        "Misol: 1234"
    )
