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

# تابع: دریافت اطلاعات سشن‌های معاملاتی
def fetch_trading_sessions():
    url = "https://market24hclock.com/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # یافتن بخش سشن‌ها
            sessions = soup.select(".sessions-table tbody tr")
            session_data = []
            
            for session in sessions:
                columns = session.find_all("td")
                if len(columns) >= 4:
                    market = columns[0].text.strip()
                    status = columns[1].text.strip()
                    open_time = columns[2].text.strip()
                    close_time = columns[3].text.strip()
                    session_data.append(
                        f"📍 بازار: {market}\n🟢 وضعیت: {status}\n⏰ باز: {open_time} - بسته: {close_time}"
                    )
            
            return "\n\n".join(session_data)
        else:
            return "❌ خطا در دریافت اطلاعات از Market24hClock"
    except Exception as e:
        return f"❌ خطا: {str(e)}"

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
                [KeyboardButton("🕒 سشن‌های معاملاتی"), KeyboardButton("🔚 خروج")]
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

# سشن‌های معاملاتی
@app.on_message(filters.command("sessions"))
def trading_sessions_command(client, message):
    sessions_info = fetch_trading_sessions()
    message.reply_text(
        f"🌍 **اطلاعات سشن‌های معاملاتی:**\n\n{sessions_info}",
        disable_web_page_preview=True
    )
@app.on_message(filters.text & filters.regex("🕒 سشن‌های معاملاتی"))
def trading_sessions(client, message):
    sessions_info = fetch_trading_sessions()
    message.reply_text(
        f"🌍 **اطلاعات سشن‌های معاملاتی:**\n\n{sessions_info}",
        disable_web_page_preview=True
    )

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
