from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Dispatcher
from keyboards import reply_keyboard, menu_categories_keyboard
from menu_loader import MenuLoader
from config import TOKEN
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = Bot(token=TOKEN)
menu_loader = MenuLoader("tary_menu2.json")

# Store user orders
user_orders = {}
user_order_total = {}

async def start(message: Message):
    text = ("\"Tary\" асханасының онлайн-даяшысын қарсы алыңыз! 🍽️\n"
            "Мен – Tary Telegram-ботымын, сіздің жеке даяшыңызбын. Мәзірді қарап, тапсырыс беріп, "
            "сүйікті тағамдарыңызды тез әрі ыңғайлы түрде ала аласыз! 😋\n\n"
            "Сізге қалай көмектесе аламын? 😊")
    await message.answer(text, reply_markup=reply_keyboard)

async def handle_menu_buttons(message: Message):
    user_id = message.from_user.id
    if message.text == "📜 View menu":
        await message.answer("📜 Мәзір санатын таңдаңыз:", reply_markup=menu_categories_keyboard())
    elif message.text == "🛒 My cart":
        if user_id not in user_orders or not user_orders[user_id]:
            await message.answer("Сіздің себетіңіз бос!")
        else:
            order_text = "\n".join(user_orders[user_id])
            total_price = user_order_total.get(user_id, 0)
            await message.answer(f"🛍 Сіздің тапсырысыңыз:\n{order_text}\n\n💰 Жалпы баға: {total_price} KZT")
    elif message.text == "📞 Contacts":
        await message.answer("Бұл бөлім әзірге дайын емес. Жақында іске қосылады! 🛠")

async def show_items(callback: CallbackQuery):
    category = callback.data
    items = menu_loader.get_items(category)
    if not items:
        await callback.message.answer("Бұл санатта тағамдар жоқ!")
        return

    for item in items:
        text = f"🍽 {item['name']}\n💰 {item['price_kzt']} KZT"
        if "description" in item:
            text += f"\n📖 {item['description']}"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Add to cart", callback_data=f"add_{item['name']}")]
        ])

        if "image_url" in item:
            await bot.send_photo(callback.message.chat.id, photo=item["image_url"], caption=text, reply_markup=keyboard)
        else:
            await callback.message.answer(text, reply_markup=keyboard)

async def add_to_cart(callback: CallbackQuery):
    item_name = callback.data.split("add_", 1)[1]
    user_id = callback.from_user.id

    if user_id not in user_orders:
        user_orders[user_id] = []
        user_order_total[user_id] = 0

    user_orders[user_id].append(item_name)
    user_order_total[user_id] += menu_loader.get_price(item_name)

    await callback.answer(f"{item_name} себетке қосылды!")

def register_handlers(dp: Dispatcher):
    dp.message.register(start, Command("start"))
    dp.message.register(handle_menu_buttons)
    dp.callback_query.register(show_items, lambda c: c.data in menu_loader.get_categories())
    dp.callback_query.register(add_to_cart, lambda c: c.data.startswith("add_"))
