from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from menu_loader import MenuLoader

# Load menu
menu_loader = MenuLoader("tary_menu.json")

# Reply Keyboard
reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📜 View menu")],
    [KeyboardButton(text="🛒 My cart")],
    [KeyboardButton(text="📞 Contacts")]
], resize_keyboard=True)

# Inline Keyboard for menu categories
def menu_categories_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=category, callback_data=category)]
        for category in menu_loader.get_categories()
    ])
