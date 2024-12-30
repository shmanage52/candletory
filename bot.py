import asyncio
import aiohttp
import requests
import json
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton


#  app اطلاعات 
API_TOKEN = "7575235119:AAGFR15l6OFkOq_8S05WXfTvoRuu4YCf0vQ"  # جایگزین کنید با کلید API خود
APP_ID = 25709855  # App ID تلگرام
APP_HASH = "740efc27f273ac589176b85853ef8088"  # App Hash تلگرام

app = Client("candletory_bot", bot_token=API_TOKEN, api_id=APP_ID, api_hash=APP_HASH)

# لیست ارزهای دیجیتال
SYMBOLS = [
    {"symbol": "mkr", "name": "Bitcoin"},
    
]

# توابع ذخیره و بارگذاری پروفایل کاربران
USER_DB = "user_profiles.json"

def load_profiles():
    try:
        with open(USER_DB, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_profiles(profiles):
    with open(USER_DB, "w") as file:
        json.dump(profiles, file, indent=4)

user_profiles = load_profiles()

# منوی اصلی
def main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📡 قیمت لحظه‌ای ارزها")],
            [KeyboardButton("💳 اشتراک VIP"), KeyboardButton("👤 پروفایل من")],
            [KeyboardButton("📨 دعوت از دوستان"), KeyboardButton("🔚 خروج")]
        ],
        resize_keyboard=True
    )

# تابع دریافت قیمت ارزها
async def fetch_prices():
    url = "https://api.nobitex.ir/market/global-stats"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            if response.status != 200:
                print(f"HTTP Error: {response.status}")  # چاپ وضعیت HTTP
                return None
            data = await response.json()
            print(data)  # چاپ داده‌ها برای بررسی ساختار
            prices = {}
            for symbol in SYMBOLS:
                key = symbol["symbol"]
                if key in data:
                    try:
                        # پردازش قیمت از ساختار داده‌ها
                        prices[key] = {
                            "price": float(data[key]["binance"]["price"]),
                            "name": symbol["name"],
                        }
                    except KeyError:
                        print(f"KeyError for symbol: {key}")
                        continue
            return prices

# دکمه قیمت لحظه‌ای ارزها
@app.on_message(filters.text & filters.regex("📡 قیمت لحظه‌ای ارزها"))
async def handle_price_button(client, message):
    prices = await fetch_prices()
    if not prices:
        print("Prices is None or Empty.")  # چاپ خطا
        await message.reply_text("❌ خطا در دریافت قیمت‌ها.")
        return

    message_text = "💹 <b>قیمت‌های ارزهای دیجیتال:</b>\n\n"
    message_text = "💹 <b>قیمت‌های ارزهای دیجیتال:</b>\n\n"
    for key, value in prices.items():
        message_text += f"🔹 {value['name']}: {value['price']} USDT\n"

    message_text += f"\n⏰ <i>آخرین به‌روزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
    await message.reply_text(message_text, parse_mode="HTML")

# دکمه دعوت از دوستان
@app.on_message(filters.text & filters.regex("📨 دعوت از دوستان"))
def invite_friends(client, message):
    user_id = str(message.from_user.id)
    invite_link = f"https://t.me/candletory_bot?start={user_id}"
    message.reply_text(
        f"🌟 **دوستان خود را دعوت کنید!**\n\n"
        f"🔗 لینک دعوت شما:\n{invite_link}\n\n"
        "✅ به ازای هر دوستی که از لینک شما استفاده کند، 1 امتیاز دریافت خواهید کرد.",
        reply_markup=main_menu()
    )

# نمایش پروفایل کاربر
@app.on_message(filters.text & filters.regex("👤 پروفایل من"))
def show_profile(client, message):
    user_id = str(message.from_user.id)
    if user_id in user_profiles:
        profile = user_profiles[user_id]
        is_premium = "بله ✅" if profile["is_premium"] else "خیر ❌"
        message.reply_text(
            f"👤 **پروفایل شما:**\n\n"
            f"📛 نام: {profile['name']}\n"
            f"🆔 آیدی: {profile['username']}\n"
            f"⭐ امتیازات: {profile['points']}\n"
            f"🌟 اشتراک VIP: {is_premium}\n"
            f"⏰ تاریخ عضویت: {profile['joined_at']}",
            reply_markup=main_menu()
        )
    else:
        message.reply_text("❌ پروفایل شما یافت نشد. لطفاً دستور /start را بزنید.")

# ارسال خودکار قیمت‌ها
async def post_prices_to_channel():
    prices = await fetch_prices()
    if not prices:
        print("خطا در دریافت قیمت‌ها")
        return

    message = "💹 <b>قیمت‌های ارزهای دیجیتال:</b>\n\n"
    for symbol, data in prices.items():
        message += f"🔹 {data['name']}: {data['price']} USDT\n"
    message += f"\n⏰ <i>آخرین به‌روزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"

    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
        payload = {"chat_id": "@candletory", "text": message, "parse_mode": "HTML"}
        async with session.post(url, json=payload) as response:
            if response.status != 200:
                print(f"خطا در ارسال پیام: {await response.text()}")

# زمان‌بندی ارسال خودکار
async def scheduler():
    while True:
        await post_prices_to_channel()
        await asyncio.sleep(300)  # هر 5 دقیقه

# شروع ربات
@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id

    if str(user_id) not in user_profiles:
        user_profiles[str(user_id)] = {
            "name": message.from_user.first_name,
            "username": message.from_user.username,
            "points": 0,
            "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_premium": False
        }
        save_profiles(user_profiles)

    message.reply_text(
        f"👋 خوش آمدید {message.from_user.first_name}!\n"
        "از منوی زیر استفاده کنید:",
        reply_markup=main_menu()
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    app.run()