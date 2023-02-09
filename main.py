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
        BotCommand(command="/start", description="Show available commands"),
        BotCommand(command="/cancel", description="Cancel any action"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting bot!")

    load_dotenv()
    API_TOKEN = os.getenv("TELE_TOKEN", "")
    ADMIN_IDS = os.getenv("APPROVED_USERS", "").split(", ")

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp, ADMIN_IDS)
    register_handlers_spending(dp, ADMIN_IDS)

    await set_commands(bot)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
