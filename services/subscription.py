import logging
from typing import List
from aiogram import Bot

logger = logging.getLogger(__name__)


async def check_user_subscriptions(bot: Bot, user_id: int, channels: List[str]) -> List[str]:
    """
    Check if user is subscribed to all channels
    Returns list of channels user is NOT subscribed to
    """
    not_subscribed = []
    
    logger.info(f"Checking subscriptions for user {user_id} in {len(channels)} channels")
    
    for channel in channels:
        try:
            logger.info(f"Checking channel: {channel}")
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            logger.info(f"User status in {channel}: {member.status}")
            
            # Check if user is member, administrator, or creator
            if member.status in ['left', 'kicked']:
                not_subscribed.append(channel)
                logger.info(f"User NOT subscribed to {channel}")
            else:
                logger.info(f"User IS subscribed to {channel}")
        except Exception as e:
            logger.error(f"Error checking subscription for {channel}: {e}")
            # If error, assume not subscribed
            not_subscribed.append(channel)
    
    logger.info(f"Not subscribed channels: {not_subscribed}")
    return not_subscribed
