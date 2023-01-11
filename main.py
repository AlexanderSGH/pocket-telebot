import os
import logging
import asyncio

from dotenv import load_dotenv

from app.handlers.spendings import register_handlers_spending
from app.handlers.common import register_handlers_common

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/add_spending", description="Add new spending"),
        BotCommand(command="/show_last_spending", description="Show last spending"),
        BotCommand(command="/remove_last_spending", description="Remove last spending"),
        BotCommand(command="/weather", description="Check local weather"),
        BotCommand(command="/fine", description="Check fines"),
        BotCommand(command="/start", description="Welcome Message"),
        BotCommand(command="/cancel", description="Cancel any action"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting bot!")

    load_dotenv()
    API_TOKEN = os.getenv("TELE_TOKEN", "")
    ADMIN_IDS = [os.getenv("USER_ONE", ""),
                 os.getenv("USER_TWO", "")]

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp, ADMIN_IDS)
    register_handlers_spending(dp, ADMIN_IDS)

    await set_commands(bot)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
