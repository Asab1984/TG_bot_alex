import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import requests
from bs4 import BeautifulSoup as bs
import json
import datetime

from config import TOKEN
from keyboards.admin_kb import main_keyboard, sec_keyboard
from database.sqlite_db import create_database, add_to_db, read_db

storage = MemoryStorage()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)


class FSMAdmin(StatesGroup):
    title = State()
    text = State()
    image = State()
    published_at = State()


@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(f'Hello, {message.from_user.full_name}', reply_markup=main_keyboard)


@dp.message(Command('Progr_langs'))
async def second_kb_show(message: Message):
    await message.answer('OK', reply_markup=sec_keyboard)


@dp.message(Command('<Back'))
async def back_func(message: Message):
    await message.answer('OK', reply_markup=main_keyboard)


@dp.message(Command('C++'))
async def cpp_read(message: Message):
    with open('database/cpp.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=sec_keyboard)


@dp.message(Command('Python'))
async def python_read(message: Message):
    with open('database/python.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=sec_keyboard)


@dp.message(Command('Java'))
async def java_read(message: Message):
    with open('database/java.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=sec_keyboard)


@dp.message(Command('PHP'))
async def php_read(message: Message):
    with open('database/php.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=sec_keyboard)


@dp.message(Command('About'))
async def php_read(message: Message):
    with open('database/about.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=sec_keyboard)


@dp.message(Command('Read_me'))
async def send_file(message: Message):
    file = FSInputFile('database/readme.txt')
    await bot.send_document(document=file, chat_id=message.from_user.id)


@dp.message(Command('Download'))
async def fs_start(message: Message, state: FSMContext):
    await state.set_state(FSMAdmin.image)
    await message.answer('Завантажте фото \n\n Припинити ввід - /Cancel')


@dp.message(Command('Cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Canceled')


@dp.message(FSMAdmin.image)
async def down_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    await state.set_state(FSMAdmin.title)
    await message.answer('Введи назву')


@dp.message(FSMAdmin.title)
async def down_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(FSMAdmin.text)
    await message.answer('Введи текст')


@dp.message(FSMAdmin.text)
async def down_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(FSMAdmin.published_at)
    await message.answer('Введи дату публікації')


@dp.message(FSMAdmin.published_at)
async def down_published_at(message: Message, state: FSMContext):
    await state.update_data(published_at=message.text)
    data = await state.get_data()
    add_to_db(data)
    await state.clear()
    await message.answer('Complete', reply_markup=main_keyboard)


@dp.message(Command('Show'))
async def show(message: Message):
    data = read_db()
    for i in data:
        await message.answer_photo(i[0],
                                   f'Назва {i[1]}\n Текст {i[2]}\n Дата {i[3]}')


@dp.message(Command('Info'))
async def show_info(message: Message):
    headers_for_parse = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"
    }
    url = 'https://pogoda.meta.ua/ua/Kyivska/Kyievo-Sviatoshynskyi/Hatne/'
    parse_url = requests.get(url, headers=headers_for_parse)
    result = bs(parse_url.text, 'html.parser')
    values = result.findAll("div", class_= "city__day fl-col active")
    drg = []
    for i in values[:2]:
        day = i.find('div', class_= 'city__day-date fl-col')
        day = day.text
        day = day.translate(str.maketrans('', '', ''.join(['\n', ' '])))

        whr_t = i.find('div', class_= "city__day-temperature")
        whr_t = whr_t.text
        whr_t = whr_t.translate(str.maketrans('', '', ''.join(['\n', ' '])))

        mess = (f' {day} {whr_t}\n')
        drg.append(mess)
    drg_string = ''.join(drg)
    await message.answer(drg_string, reply_markup=main_keyboard)


####################
@dp.message()
async def echo_message(message: Message):
    await message.answer(message.text)

# function for bot starting
async def main():
    print('BOT online')
    create_database()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())




