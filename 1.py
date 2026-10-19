import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import asyncio
from aiogram import Bot, Dispatcher, Fh
from buttons import main_menu, school_lessons_buttons

bot = Bot(token="8753784106:AAFtcRo75PgKSpkutUAkfSxyJxmyS4TKzh0")
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: Message):
    full_name = message.from_user.full_name
    await message.answer(f"Xush kelibsiz! {full_name}", reply_markup=await main_menu())


@dp.callback_query(F.data == "school_lessons")
async def reaction_to_school_lessons(call: CallbackQuery):
    await call.message.answer("Sinfni tanlang!", reply_markup=await school_lessons_buttons())


@dp.callback_query(F.data.startswith("lesson_"))
async def reaction_to_lesson(call: CallbackQuery):
    class_id = int(call.data.split("_")[-1])
   
    if class_id == 1:
        print(1)
    elif class_id == 2:
        print(2)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
