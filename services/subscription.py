import logging
from typing import List, Tuple
from aiogram import Bot

logger = logging.getLogger(__name__)


async def check_user_subscriptions(bot: Bot, user_id: int, channels: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
    """
    Check if user is subscribed to all channels
    channels: List of (channel_id, username, title) tuples
    Returns list of channels user is NOT subscribed to
    """
    not_subscribed = []
    
    logger.info(f"Checking subscriptions for user {user_id} in {len(channels)} channels")
    
    for channel in channels:
        channel_id, username, title = channel
        try:
            logger.info(f"Checking channel: {channel_id}")
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            logger.info(f"User status in {channel_id}: {member.status}")
            
            # Check if user is member, administrator, or creator
            if member.status in ['left', 'kicked']:
                not_subscribed.append(channel)
                logger.info(f"User NOT subscribed to {channel_id}")
            else:
                logger.info(f"User IS subscribed to {channel_id}")
        except Exception as e:
            logger.error(f"Error checking subscription for {channel_id}: {e}")
            # If error, assume not subscribed
            not_subscribed.append(channel)
    
    logger.info(f"Not subscribed channels: {not_subscribed}")
    return not_subscribed
