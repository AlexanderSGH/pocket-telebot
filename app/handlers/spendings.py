from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup


spending_categories = ['Продукты','Медицина','Заказы','Транспорт','Дом',
                       'Одежда','Техника','Развлечения','Подарки','Кафе']


class AddSpending(StatesGroup):
    waiting_for_spending_category = State()
    waiting_for_spending_amount = State()


async def spending_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         input_field_placeholder="Select category")
    keyboard.add(*spending_categories)
    await message.answer("Choose spending category", reply_markup=keyboard)
    await state.set_state(AddSpending.waiting_for_spending_category.state)


async def spending_category_chosen(message: types.Message, state: FSMContext):
    if message.text not in spending_categories:
        await message.answer("Please select the appropriate category")
        return
    await state.update_data(chosen_category=message.text)
    await state.set_state(AddSpending.waiting_for_spending_amount.state)
    await message.answer("Now enter the amount of expenses",
                         reply_markup=types.ReplyKeyboardRemove())


async def spending_amount_chosen(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Please enter the correct amount")
        return
    user_data = await state.get_data()
    await message.answer(f"You have selected {user_data['chosen_category']}.\n"
                         f"And the amount was {message.text}")
    await state.finish()


def register_handlers_spending(dp: Dispatcher, admin_id: list):
    dp.register_message_handler(spending_start, IDFilter(user_id=admin_id),
                                commands="add_spending", state="*")
    dp.register_message_handler(spending_category_chosen, IDFilter(user_id=admin_id),
                                state=AddSpending.waiting_for_spending_category)
    dp.register_message_handler(spending_amount_chosen, IDFilter(user_id=admin_id),
                                state=AddSpending.waiting_for_spending_amount)
