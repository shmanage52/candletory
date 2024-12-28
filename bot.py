import time
from turtle import pd
import requests
import json
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


# اطلاعات 
API_TOKEN = "7575235119:AAGFR15l6OFkOq_8S05WXfTvoRuu4YCf0vQ"  # جایگزین کنید با کلید API خود
APP_ID = 25709855  # App ID تلگرام
APP_HASH = "740efc27f273ac589176b85853ef8088"  # App Hash تلگرام

# تعریف دیکشنری برای ذخیره پروفایل کاربران
user_profiles = {}
save_profiles = {}

# راه‌اندازی 
app = Client("candletory_bot", bot_token=API_TOKEN, api_id=APP_ID, api_hash=APP_HASH)


# تابع برای دکمه‌های بازگشت به منوی اصلی
def add_back_to_main_menu(buttons):
    back_button = [KeyboardButton("🔙 بازگشت به منوی اصلی")]
    buttons.append(back_button)  # دکمه "بازگشت به منوی اصلی" را به انتهای دکمه‌ها اضافه می‌کند
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
# منوی اصلی
@app.on_message(filters.text & filters.regex("📋 منوی اصلی"))
def main_menu(client, message):
    buttons = [
        [KeyboardButton("📨 دعوت از دوستان")],
        [KeyboardButton("📊 وضعیت امتیازات")]
    ]
    message.reply_text(
        "👋 خوش آمدید به ربات ما! لطفاً یکی از گزینه‌ها را انتخاب کنید.",
        reply_markup=add_back_to_main_menu(buttons)
    )
    
# لیست ارزهای دیجیتال
crypto_list = ['bitcoin', 'ethereum', 'dogecoin', 'litecoin', 'ripple', 'cardano', 'polkadot', 'solana', 'shiba-inu', 'binancecoin', 'tron', 'uniswap', 'chainlink', 'monero', 'vechain', 'tether', 'stellar', 'aave', 'sushi']

# تابع برای دریافت قیمت لحظه‌ای ارز
def get_crypto_price(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if crypto in data:
            return data[crypto]['usd']
    return None

# تابع برای دریافت قیمت تاریخچه‌ای و رسم نمودار
def get_price_history(crypto):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days=7"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'prices' in data:
            prices = data['prices']
            dates = [item[0] for item in prices]  # استخراج تاریخ‌ها
            values = [item[1] for item in prices]  # استخراج قیمت‌ها
            return dates, values
    return [], []

# تابع برای رسم نمودار
def plot_price_chart(dates, prices, crypto_name):
    # تبدیل زمان Unix به فرمت خوانا
    formatted_dates = [pd.to_datetime(date, unit='ms').strftime('%Y-%m-%d') for date in dates]

    plt.figure(figsize=(10, 6))
    plt.plot(formatted_dates, prices, label=f"{crypto_name} Price", color='blue')
    plt.title(f"نمودار قیمت {crypto_name} در 7 روز گذشته")
    plt.xlabel("تاریخ")
    plt.ylabel("قیمت (USD)")
    plt.xticks(rotation=45)  # چرخش تاریخ‌ها برای خوانایی بهتر
    plt.legend()
    plt.grid(True)

    # ذخیره نمودار به صورت تصویر
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()  # پاکسازی حافظه برای نمودارهای بعدی
    img.seek(0)
    return img

# تست کد
if __name__ == "__main__":
    crypto = "bitcoin"
    dates, prices = get_price_history(crypto)
    if dates and prices:
        img = plot_price_chart(dates, prices, crypto)
        with open(f"{crypto}_chart.png", "wb") as f:
            f.write(img.getbuffer())
        print(f"نمودار قیمت {crypto} ذخیره شد.")
    else:
        print("خطا در دریافت داده‌ها.")

# نمایش لیست منوها به کاربر
@app.on_message(filters.command("start"))
def start(client, message):
    keyboard = [
        [KeyboardButton("💱 نرخ لحظه ای ارز دیجیتال")],
        [KeyboardButton("📡 دریافت اطلاعات API"), KeyboardButton("💳 اشتراک VIP")],
        [KeyboardButton("👤 پروفایل من"), KeyboardButton("📨 دعوت از دوستان")],
        [KeyboardButton("🔚 خروج")],
    ]
    message.reply_text(
        f"👋 خوش آمدید {message.from_user.first_name}!\n"
        "از منوی زیر استفاده کنید:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# نمایش لیست ارزهای دیجیتال به کاربر
@app.on_message(filters.text & filters.regex("💱 نرخ لحظه ای ارز دیجیتال"))
def show_crypto_list(client, message):
    keyboard = []
    for crypto in crypto_list:
        price = get_crypto_price(crypto)
        price_text = f"${price}" if price else "قیمت در دسترس نیست"
        keyboard.append([KeyboardButton(f"{crypto.capitalize()}: {price_text}")])

    message.reply_text(
        "لیست ارزهای دیجیتال معروف و قیمت‌های آن‌ها:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# نمایش نمودار پس از انتخاب ارز
@app.on_message(filters.text & filters.regex('|'.join([crypto.capitalize() for crypto in crypto_list])))
def show_chart(client, message):
    crypto_name = message.text.split(":")[0].strip().lower()  # نام ارز انتخاب شده
    price_history = get_price_history(crypto_name)

    if price_history:
        img = plot_price_chart(price_history, crypto_name)
        message.reply_photo(img, caption=f"نمودار قیمت {crypto_name.capitalize()} در 7 روز گذشته:")
    else:
        message.reply_text(f"❌ نتواستم تاریخچه قیمت {crypto_name.capitalize()} رو پیدا کنم.")


# ذخیره پروفایل کاربران در فایل
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

# تابع ایجاد یا بازیابی پروفایل کاربر
@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id

    # بررسی دعوت
    if len(message.command) > 1:
        referrer_id = message.command[1]
        if referrer_id != str(user_id) and referrer_id in user_profiles:
            user_profiles[referrer_id]["points"] += 1
            save_profiles(user_profiles)

# ایجاد پروفایل جدید اگر وجود نداشته باشد
    if str(user_id) not in user_profiles:
        user_profiles[str(user_id)] = {
            "name": message.from_user.first_name,
            "username": message.from_user.username,
            "points": 0,
            "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_premium": False
        }
        save_profiles(user_profiles)  # ذخیره پروفایل در فایل

    message.reply_text(
        f"👋 خوش آمدید {message.from_user.first_name}!\n"
        "از منوی زیر استفاده کنید:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("📡 دریافت اطلاعات API"), KeyboardButton("💳 اشتراک VIP")],
                [KeyboardButton("👤 پروفایل من"), KeyboardButton("📨 دعوت از دوستان")],
                [KeyboardButton("🔚 خروج")]
            ],
            resize_keyboard=True
        )
    )

# نمایش پروفایل کاربر
@app.on_message(filters.text & filters.regex("👤 پروفایل من"))
def show_profile(client, message):
    user_id = str(message.from_user.id)
    if user_id in user_profiles:
        profile = user_profiles[user_id]
        is_premium = "بله ✅" if profile["is_premium"] else "خیر ❌"
        buttons = [
            [KeyboardButton("📊 نمایش امتیازات")],  # دکمه‌های اضافی
            [KeyboardButton("💳 ارتقا به VIP")]
        ]
        message.reply_text(
            f"👤 **پروفایل شما:**\n\n"
            f"📛 نام: {profile['name']}\n"
            f"🆔 آیدی: {profile['username']}\n"
            f"⭐ امتیازات: {profile['points']}\n"
            f"🌟 اشتراک VIP: {is_premium}\n"
            f"⏰ تاریخ عضویت: {profile['joined_at']}",
        )
    else:
        print(f"Profile not found for user: {user_id}")  # لاگ عدم وجود پروفایل
        message.reply_text("❌ پروفایل شما یافت نشد. لطفاً دستور /start را بزنید.")


# دعوت از دوستان
@app.on_message(filters.text & filters.regex("📨 دعوت از دوستان"))
def invite_friends(client, message):
    user_id = str(message.from_user.id)
    invite_link = f"https://t.me/candletory_bot?start={user_id}"  # لینک دعوت
    buttons = [
        [KeyboardButton("👥 بررسی دعوت‌ها")]  # دکمه شیشه‌ای
    ]
    message.reply_text(
        f"🌟 **دوستان خود را دعوت کنید!**\n\n"
        f"🔗 لینک دعوت شما:\n{invite_link}\n\n"
        "✅ به ازای هر دوستی که از لینک شما استفاده کند، 1 امتیاز دریافت خواهید کرد.",
        reply_markup=add_back_to_main_menu(buttons)  # افزودن دکمه‌ها
    )

# هنگامی که کاربر روی دکمه "بازگشت به منوی اصلی" کلیک می‌کند
@app.on_message(filters.text & filters.regex("🔙 بازگشت به منوی اصلی"))
def return_to_main_menu(client, message):
    buttons = [
        [KeyboardButton("📨 دعوت از دوستان")],
        [KeyboardButton("📊 وضعیت امتیازات")]
    ]
    message.reply_text(
        "👋 شما به منوی اصلی برگشتید! لطفاً یکی از گزینه‌ها را انتخاب کنید.",
        reply_markup=add_back_to_main_menu(buttons)
    )

if __name__ == "__main__":
    app.run()

# پرداخت برای اشتراک VIP
@app.on_message(filters.text & filters.regex("💳 اشتراک VIP"))
def buy_vip(client, message):
    message.reply_text(
        "🌟 **اشتراک VIP:**\n"
        "برای فعال‌سازی اشتراک VIP، پرداخت خود را از طریق لینک زیر انجام دهید:\n"
        "[لینک پرداخت](https://candletory.com/pay)\n\n"
        "پس از پرداخت، رسید خود را ارسال کنید."
    )

# بررسی اشتراک VIP
@app.on_message(filters.text & filters.regex("بررسی پرداخت"))
def check_payment(client, message):
    user_id = str(message.from_user.id)
    if user_id in user_profiles:
        # بررسی پرداخت: این بخش باید با API پرداخت شما ادغام شود
        # فرض می‌کنیم پرداخت موفق باشد:
        user_profiles[user_id]["is_premium"] = True
        save_profiles(user_profiles)
        message.reply_text("✅ اشتراک VIP شما فعال شد!")
    else:
        message.reply_text("❌ پروفایل شما یافت نشد. لطفاً دستور /start را بزنید.")

# دریافت داده از API
@app.on_message(filters.text & filters.regex("📡 دریافت اطلاعات API"))
def fetch_api_data(client, message):
    api_url = "https://api.example.com/data"  # جایگزین با URL API شما
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # جایگزین با کلید API
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()  # فرض می‌کنیم پاسخ JSON است
            message.reply_text(f"📊 **نتایج API:**\n\n{json.dumps(data, indent=4)}")
        else:
            message.reply_text(f"❌ خطا در دریافت اطلاعات: {response.status_code}")
    except Exception as e:
        message.reply_text(f"❌ خطای اتصال: {str(e)}")

# خروج از ربات
@app.on_message(filters.text & filters.regex("🔚 خروج"))
def exit_bot(client, message):
    message.reply_text("🚪 از ربات خارج شدید. برای بازگشت، /start را بزنید.")

# اجرای ربات
app.run()