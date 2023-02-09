from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter, Text


COMMAND_CATEGORIES = [
    "📝 Manage spendings",
    "⛅ Weather forecast",
    "👮 Check fines",
    "❌ Cancel",
]


async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, input_field_placeholder="Select command"
    )
    keyboard.add(*COMMAND_CATEGORIES)
    await state.finish()
    await message.answer("Select an available command", reply_markup=keyboard)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Canceled!", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher, admin_id: list):
    dp.register_message_handler(
        cmd_start, IDFilter(user_id=admin_id), commands="start", state="*"
    )
    dp.register_message_handler(
        cmd_cancel, IDFilter(user_id=admin_id), commands="cancel", state="*"
    )
    dp.register_message_handler(
        cmd_cancel,
        IDFilter(user_id=admin_id),
        Text(endswith="cancel", ignore_case=True),
        state="*",
    )
