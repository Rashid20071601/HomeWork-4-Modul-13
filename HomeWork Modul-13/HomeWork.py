# Импорт библиотек
from aiogram import Bot, Dispatcher, executor, types  # Основные модули для работы с Telegram Bot API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio


# Создание объектов бота и диспетчера
api = 'Token'  # Токен Telegram-бота
bot = Bot(token=api)  # Инициализация бота
dp = Dispatcher(bot, storage=MemoryStorage())  # Инициализация диспетчера с хранением состояний
# =====================================================================================================
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Обработка сообщений
@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message)
    data = await state.get_data()
    result = round(10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']) + 5, 2)
    await message.answer(f'Ваша норма калорий {result}')
    await state.finish()

# =====================================================================================================
# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # Запуск long-polling для обработки сообщений
