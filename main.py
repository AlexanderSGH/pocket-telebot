import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELE_TOKEN")

bot = Bot(token=API_TOKEN if API_TOKEN else "")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(message.text)

def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
