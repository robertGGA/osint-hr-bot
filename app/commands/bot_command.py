from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot): 
    commands = [
        BotCommand(command='start', description='Начало работы'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='find_company', description='Поиск по компании'),
        BotCommand(command='find_employee', description='Поиск по сотруднику')
    ]