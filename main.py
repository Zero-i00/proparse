from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv
import os

load_dotenv()

token = os.environ.get("TOKEN")
bot = Bot(token=token)
storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)


class Form(StatesGroup):
    name = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer('привет')



@dp.message_handler(commands=['add'])
async def add_anime(message: types.Message):
    await Form.name.set()
    await message.answer("Введи название аниме")


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        with open("anime", 'a', encoding="utf-8") as file:
            file.write(message.text + "\n")

        await message.answer("Аниме добавлено")
        await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


