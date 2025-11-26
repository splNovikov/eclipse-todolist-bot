import asyncio
import logging
import os
from aiogram import Bot, Dispatcher

from database import Database
from handlers import router, db


async def main():
    # Get bot token from environment
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN environment variable is not set!")
    
    # Initialize database
    await db.init_db()
    logging.info("Database initialized")
    
    # Initialize bot and dispatcher (without parse mode to avoid HTML parsing issues)
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    
    # Register handlers
    dp.include_router(router)
    
    # Start polling
    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    asyncio.run(main())
