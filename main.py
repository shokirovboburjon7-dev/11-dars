import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

TOKEN = "8984302315:AAEsFPi5pCOkeVTAT2hcY6cUCdSlnxH6ff4"

router = Router()


class SchoolState(StatesGroup):
  waiting_for_grade = State()


def get_main_menu():
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [InlineKeyboardButton(text="IT Course", callback_data="it_course")],
          [
              InlineKeyboardButton(
                  text="IELTS Course", callback_data="ielts_course"
              )
          ],
          [
              InlineKeyboardButton(
                  text="Maktab darsliklari", callback_data="school_books"
              )
          ],
      ]
  )
  return keyboard



def get_grades_menu():
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(text="1-sinf", callback_data="grade_1"),
              InlineKeyboardButton(text="2-sinf", callback_data="grade_2"),
          ],
          [
              InlineKeyboardButton(text="3-sinf", callback_data="grade_3"),
              InlineKeyboardButton(text="4-sinf", callback_data="grade_4"),
          ],
          [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")],
      ]
  )
  return keyboard


@router.message(CommandStart())
async def command_start_handler(message: Message):
  await message.answer(
      "Assalomu alaykum! Kerakli tugmani tanlang:", reply_markup=get_main_menu()
  )


# 1. IT Course bosilganda
@router.callback_query(F.data == "it_course")
async def process_it_course(callback: CallbackQuery):
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="Python dasturlash", callback_data="sub_python"
              )
          ],
          [
              InlineKeyboardButton(
                  text="Frontend dasturlash", callback_data="sub_frontend"
              )
          ],
          [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")],
      ]
  )
  await callback.message.edit_text(
      "IT Course yo'nalishlari:", reply_markup=keyboard
  )
  await callback.answer()


# 2. IELTS Course bosilganda
@router.callback_query(F.data == "ielts_course")
async def process_ielts_course(callback: CallbackQuery):
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="General IELTS", callback_data="sub_general"
              )
          ],
          [
              InlineKeyboardButton(
                  text="Intensive IELTS", callback_data="sub_intensive"
              )
          ],
          [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")],
      ]
  )
  await callback.message.edit_text(
      "IELTS Course yo'nalishlari:", reply_markup=keyboard
  )
  await callback.answer()


# 3. Maktab darsliklari bosilganda (Sinf tugmalarini chiqarish va statega o'tish)
@router.callback_query(F.data == "school_books")
async def process_school_books(callback: CallbackQuery, state: FSMContext):
  await callback.message.edit_text(
      "Sinfni tanlang (1 dan 4-sinfgacha):", reply_markup=get_grades_menu()
  )
  await state.set_state(SchoolState.waiting_for_grade)
  await callback.answer()


# Sinflar bosilganda har biriga bittadan rasm yuborish
@router.callback_query(
    SchoolState.waiting_for_grade, F.data.startswith("grade_")
)
async def process_grade_selection(callback: CallbackQuery, state: FSMContext):
  grade = callback.data.split("_")[1]

  # Eslatma: Kompyuteringizda shu nomdagi rasmlar bo'lishi kerak yoki to'g'ridan-to'g'ri rasm havolasini (URL) yuborishingiz mumkin.
  # Misol uchun internetdagi rasm havolasini ham berishingiz mumkin: InputFile yoki to'g'ridan-to'g'ri URL matn ko'rinishida:
  photos = {
      "1": "https://picsum.photos/id/10/400/300",
      "2": "https://picsum.photos/id/20/400/300",
      "3": "https://picsum.photos/id/30/400/300",
      "4": "https://picsum.photos/id/40/400/300",
  }

  photo_url = photos.get(grade, "https://picsum.photos/400/300")

  await callback.message.answer_photo(
      photo=photo_url, caption=f"Mana {grade}-sinf uchun darslik rasmi!"
  )
  await state.clear()
  await callback.answer()


# Orqaga qaytish tugmasi
@router.callback_query(F.data == "back_to_main")
async def process_back(callback: CallbackQuery, state: FSMContext):
  await state.clear()
  await callback.message.edit_text(
      "Asosiy menyu:", reply_markup=get_main_menu()
  )
  await callback.answer()


async def main():
  bot = Bot(token=TOKEN)
  dp = Dispatcher()
  dp.include_router(router)
  print("Bot ishga tushdi...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())