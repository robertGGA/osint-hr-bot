from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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