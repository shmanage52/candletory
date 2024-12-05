import time
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests
from bs4 import BeautifulSoup

# اطلاعات ربات
API_TOKEN = "7575235119:AAGFR15l6OFkOq_8S05WXfTvoRuu4YCf0vQ"
APP_ID = 25709855
APP_HASH = "740efc27f273ac589176b85853ef8088"
CHANNEL_USERNAME = "@Candletory"  # نام کاربری کانال

# راه‌اندازی ربات
app = Client("candletory_bot", bot_token=API_TOKEN, api_id=APP_ID, api_hash=APP_HASH)

# تابع دریافت سیگنال‌ها از MQL5
def fetch_newest_signals():
    url = "https://www.mql5.com/en/signals"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            signal_elements = soup.select(".signal-entry-title a")
            references = [signal.text.strip() for signal in signal_elements]
            return references[:5]  # پنج سیگنال اول
        else:
            print("❌ خطا در دریافت سیگنال‌ها")
            return None
    except Exception as e:
        print(f"❌ خطا در اتصال به سایت: {e}")
        return None

# ارسال پیام به کانال
def send_signal_to_group(signal):
    try:
        message = f"📢 سیگنال جدید: {signal}\n🌐 [مشاهده سیگنال در MQL5](https://www.mql5.com/en/signals)"
        app.send_message(CHANNEL_USERNAME, message, disable_web_page_preview=True)
    except Exception as e:
        print(f"❌ خطا در ارسال پیام: {e}")

# تنظیمات ارسال خودکار
def auto_post_signals():
    signals = fetch_newest_signals()
    if signals:
        for signal in signals:
            send_signal_to_group(signal)
            time.sleep(5)  # فاصله زمانی بین ارسال‌ها
    else:
        print("❌ سیگنال جدیدی پیدا نشد.")

# دستور شروع
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text(
        "👋 خوش آمدید به ربات Candletory!\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("📡 دریافت سیگنال‌ها"), KeyboardButton("🚀 شروع ارسال خودکار")],
                [KeyboardButton("🔚 خروج")]
            ],
            resize_keyboard=True
        )
    )

# دریافت سیگنال‌ها
@app.on_message(filters.text & filters.regex("📡 دریافت سیگنال‌ها"))
def get_signals(client, message):
    signals = fetch_newest_signals()
    if signals:
        signal_text = "\n".join([f"🔹 {signal}" for signal in signals])
        message.reply_text(
            f"📢 **سیگنال‌های جدید:**\n\n{signal_text}\n\n🌐 [مشاهده سیگنال‌ها در MQL5](https://www.mql5.com/en/signals)",
            disable_web_page_preview=True
        )
    else:
        message.reply_text("❌ سیگنال جدیدی پیدا نشد.")

# شروع ارسال خودکار
@app.on_message(filters.text & filters.regex("🚀 شروع ارسال خودکار"))
def start_auto_signals(client, message):
    message.reply_text("✅ ارسال خودکار سیگنال‌ها شروع شد!")
    auto_post_signals()

# خروج
@app.on_message(filters.text & filters.regex("🔚 خروج"))
def exit_bot(client, message):
    message.reply_text("🚪 از ربات خارج شدید.\nبرای بازگشت، /start را بزنید.")

# اجرای ربات
app.run()
