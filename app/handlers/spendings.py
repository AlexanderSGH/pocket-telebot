from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter, Text
from aiogram.dispatcher.filters.state import State, StatesGroup

PASS_BUTTON = "Pass"
SPENDING_COMMANDS = [
    "๐ Add spending",
    "๐ Show last spending",
    "๐๏ธ Remove last spending",
    "๐ Show all categories",
]
SPENDING_CATEGORIES = {
    "๐ Groceries": "Mostly food",
    "๐ Car": "Fuel and maintenance",
    "๐ช Snacks": "Including sweet",
    "๐งน Household": "Chemicals, consumables and so on",
    "๐ Transportation": "Travel by public transport",
    "๐ Outside Food": "Any cafes, restaurants or home delivery",
    "๐ฉบ Health Care": "Medications and doctor's appointments",
    "๐ Cat": "Any cat expenses",
    "๐ Clothes": "Any clothing, shoes or underwear",
    "๐  Home": "Furniture, interior items and repair of household appliances",
    "๐ป Cosumer electronics": "Appliances for yourself and for home",
    "๐ญ Entertainment": "Cinemas, museums, zoos and so on",
    "๐ Gifts": "For friends and family",
    "๐ฅ Personal": "Something out of categories for us",
    "๐ Monthly bills": "Payment for the Internet, utilities, communications",
    "โ Cancel": "Just cancel action",
}


class AddSpending(StatesGroup):
    waiting_for_spending_category = State()
    waiting_for_spending_amount = State()
    waiting_for_commentary = State()


async def spending_manage(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, input_field_placeholder="Select command"
    )
    keyboard.add(*SPENDING_COMMANDS)
    await message.answer("Choose spending command", reply_markup=keyboard)


async def spending_categories(message: types.Message, state: FSMContext):
    await state.finish()
    answer = "All categories:\n"
    for key, value in SPENDING_CATEGORIES.items():
        answer += f"{key}: {value}\n\n"
    await message.answer(answer)


async def spending_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, input_field_placeholder="Select category"
    )
    keyboard.add(*SPENDING_CATEGORIES.keys())
    await state.set_state(AddSpending.waiting_for_spending_category.state)
    await message.answer("Choose spending category", reply_markup=keyboard)


async def spending_category_chosen(message: types.Message, state: FSMContext):
    if message.text not in SPENDING_CATEGORIES.keys():
        await message.answer("Please select the appropriate category")
        return
    await state.update_data(chosen_category=message.text)
    await state.set_state(AddSpending.waiting_for_spending_amount.state)
    await message.answer(
        "Enter the amount of expenses", reply_markup=types.ReplyKeyboardRemove()
    )


async def spending_amount_chosen(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Please enter the correct amount")
        return
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
    )
    keyboard.add(PASS_BUTTON)
    await state.update_data(spending_amount=message.text)
    await state.set_state(AddSpending.waiting_for_commentary.state)
    await message.answer("Any commentary?", reply_markup=keyboard)


async def spending_commentary(message: types.Message, state: FSMContext):
    if message.text == PASS_BUTTON:
        pass
    user_data = await state.get_data()
    await message.answer(
        f"You have selected {user_data['chosen_category']}.\n"
        f"Amount was {user_data['spending_amount']}.\n"
        f"And the commentary - {message.text}",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


def register_handlers_spending(dp: Dispatcher, admin_id: list):
    dp.register_message_handler(
        spending_manage,
        IDFilter(user_id=admin_id),
        Text(endswith=" Manage spendings", ignore_case=True),
        state="*",
    )
    dp.register_message_handler(
        spending_categories,
        IDFilter(user_id=admin_id),
        Text(endswith=" Show all categories", ignore_case=True),
        state="*",
    )
    dp.register_message_handler(
        # TODO function with DB
        spending_categories,
        IDFilter(user_id=admin_id),
        Text(endswith=" Show last spending", ignore_case=True),
        state="*",
    )
    dp.register_message_handler(
        # TODO function with DB
        spending_categories,
        IDFilter(user_id=admin_id),
        Text(endswith=" Remove last spending", ignore_case=True),
        state="*",
    )
    dp.register_message_handler(
        spending_start,
        IDFilter(user_id=admin_id),
        Text(endswith=" Add spending", ignore_case=True),
        state="*",
    )
    dp.register_message_handler(
        spending_category_chosen,
        IDFilter(user_id=admin_id),
        state=AddSpending.waiting_for_spending_category,
    )
    dp.register_message_handler(
        spending_amount_chosen,
        IDFilter(user_id=admin_id),
        state=AddSpending.waiting_for_spending_amount,
    )
    dp.register_message_handler(
        spending_commentary,
        IDFilter(user_id=admin_id),
        state=AddSpending.waiting_for_commentary,
    )
