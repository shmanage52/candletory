import time
import requests
import json
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

# اطلاعات 
API_TOKEN = "7575235119:AAGFR15l6OFkOq_8S05WXfTvoRuu4YCf0vQ"  # جایگزین کنید با کلید API خود
APP_ID = 25709855  # App ID تلگرام
APP_HASH = "740efc27f273ac589176b85853ef8088"  # App Hash تلگرام

# راه‌اندازی 
app = Client("candletory_bot", bot_token=API_TOKEN, api_id=APP_ID, api_hash=APP_HASH)

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

@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id

    # بررسی یا ایجاد پروفایل کاربر
    if str(user_id) not in user_profiles:
        user_profiles[str(user_id)] = {
            "name": message.from_user.first_name,
            "username": message.from_user.username,
            "points": 0,
            "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_profiles(user_profiles)

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
        message.reply_text(
            f"👤 **پروفایل شما:**\n\n"
            f"🆔 آیدی: {profile['username']}\n"
            f"📛 نام: {profile['name']}\n"
            f"🌟 اشتراک VIP: {is_premium}\n"
            f"⏰ تاریخ عضویت: {profile['joined_at']}"
        )
    else:
        message.reply_text("❌ پروفایل شما یافت نشد. لطفاً دستور /start را بزنید.")

# پرداخت برای اشتراک VIP
@app.on_message(filters.text & filters.regex("💳 اشتراک VIP"))
def buy_vip(client, message):
    message.reply_text(
        "🌟 **اشتراک VIP:**\n"
        "برای فعال‌سازی اشتراک VIP، پرداخت خود را از طریق لینک زیر انجام دهید:\n"
        "[لینک پرداخت](https://candletory.com/payment)\n\n"
        "پس از پرداخت، رسید خود را ارسال کنید."
    )

# بررسی اشتراک VIP
@app.on_message(filters.text & filters.regex("بررسی پرداخت"))
def check_payment(client, message):
    user_id = str(message.from_user.id)
    if user_id in user_profiles:
        # بررسی پرداخت: این بخش باید با API پرداخت شما ادغام شود
        # به‌صورت پیش‌فرض فرض می‌کنیم پرداخت موفق باشد:
        user_profiles[user_id]["is_premium"] = True
        save_profiles(user_profiles)
        message.reply_text("✅ اشتراک VIP شما فعال شد!")
    else:
        message.reply_text("❌ پروفایل شما یافت نشد. لطفاً دستور /start را بزنید.")

# استفاده از API برای داده‌ها
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

# 📨 دعوت از دوستان"
@app.on_message(filters.text & filters.regex("📨 دعوت از دوستان"))
def invite_friends(client, message):
    user_id = str(message.from_user.id)
    invite_link = f"https://t.me/candletory_bot?start={user_id}"  # جایگزین با نام کاربری ربات
    message.reply_text(
        f"🌟 **دوستان خود را دعوت کنید!**\n\n"
        f"🔗 لینک دعوت شما:\n{invite_link}\n\n"
        "✅ به ازای هر دوستی که از لینک شما استفاده کند، 1 امتیاز دریافت خواهید کرد."
    )        

# خروج از ربات
@app.on_message(filters.text & filters.regex("🔚 خروج"))
def exit_bot(client, message):
    message.reply_text("🚪 از ربات خارج شدید. برای بازگشت، /start را بزنید.")

# اجرای ربات
app.run()