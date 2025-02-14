import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import register_handlers

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Register handlers
register_handlers(dp)

# Start bot polling
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
