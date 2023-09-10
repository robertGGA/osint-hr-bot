import asyncio
import logging
import sys
from os import getenv
import aiohttp
import json


from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from openpyxl import Workbook
from typing import Any


# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6177093910:AAGIb_a5x9P4rW75FrZspTLYE6VB9bomGv8"

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def fetch_data():
    url = 'https://jsonplaceholder.typicode.com/todos/1'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None

async def convert_json(json: Any, query: types.CallbackQuery):

    workbook = Workbook()
    sheet = workbook.active

    # Предположим, что JSON содержит список словарей, где каждый словарь представляет строку в таблице.
    for row_index, data_row in enumerate(json, start=1):
        for col_index, value in enumerate(data_row.values(), start=1):
            sheet.cell(row=row_index, column=col_index, value=value)

    # Шаг 3: Сохранить XLSX файл
    filename = 'data.xlsx'
    workbook.save(filename)

    with open(filename, 'rb') as file:
        await bot.send_document(query.from_user.id, file)



def get_select_categories():
    select_category = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Найти компанию",
                callback_data="/find_company"
            )
        ],
        [
            InlineKeyboardButton(
                text="Найти сотрудника",
                callback_data="/find_employee"
            )
        ]
    ])


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    select_category = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Найти компанию",
                callback_data="/find_company"
            )
        ],
        [
            InlineKeyboardButton(
                text="Найти сотрудника",
                callback_data="/find_employee"
            )
        ]
    ])
    await message.answer("Привет, это бот для поиска твоих будущих <b> коллег </b> или работадателей", reply_markup=select_category)


async def find_companies(query: types.CallbackQuery) -> None:
     select_category = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Пробить по ИНН",
                callback_data="/find_company_by_inn"
            ),
             InlineKeyboardButton(
                text="Пробить по ",
                callback_data="/find_company_by_inn"
            )
        ]
    ])
     await query.message.delete()
     await bot.send_message(query.from_user.id, "Все варианты проверки:", reply_markup=select_category)

async def find_employee(query: types.CallbackQuery) -> None:
     select_category = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Вернуться назад",
                callback_data="/menu"
            ),
            InlineKeyboardButton(
                text="Пробить по ИНН",
                callback_data="/find_employee_by_inn"
            ),
             InlineKeyboardButton(
                text="Пробить по номеру",
                callback_data="/find_employee_by_phone"
            )
        ]
    ])
     user_id = query.message.from_user.id
     await query.message.delete()
     await bot.send_message(query.from_user.id, "Все варианты проверки:", reply_markup=select_category)

async def find_employee_by_inn(query: types.CallbackQuery) -> None:
    data = await fetch_data()
    if data:
        await query.message.delete()
        await bot.send_message(query.from_user.id, f'<b>Вот что нашлось по вашему запросу:</b>', parse_mode="HTML")
        await convert_json(data, query)
    
    else:
        await bot.send_message(query.from_user.id, f'Ничего не найдено', parse_mode="HTML")




async def main() -> None:
    commands = [
        BotCommand(command='start', description='Начало работы'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='find_company', description='Поиск по компании'),
        BotCommand(command='find_employee', description='Поиск по сотруднику')
    ]

    dp.callback_query.register(find_companies, F.data == '/find_company')
    dp.callback_query.register(find_employee, F.data == '/find_employee')
    # dp.callback_query.register(find_employee, F.data == '/find_employee_by_phone')
    dp.callback_query.register(find_employee_by_inn, F.data == '/find_employee_by_inn')
   
    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close
    



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
