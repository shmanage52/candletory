from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
import requests
import datetime
import pytz
from bs4 import BeautifulSoup

# Bot token
TOKEN = '7575235119:AAGFR15l6OFkOq_8S05WXfTvoRuu4YCf0vQ'

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    welcome_message = (
        f"\U0001F44B خوش آمدید {user.first_name}! \n"
        "این ربات CandleTory است. از منوی زیر برای دسترسی به امکانات مختلف استفاده کنید."
    )
    keyboard = [
        [InlineKeyboardButton("\U0001F4B8 قیمت ارز و کریپتو", callback_data='crypto_prices')],
        [InlineKeyboardButton("\U0001F947 قیمت طلا و سکه", callback_data='gold_prices')],
        [InlineKeyboardButton("\U0001F4F0 اخبار فارکس", callback_data='forex_news')],
        [InlineKeyboardButton("\U0001F464 پروفایل من", callback_data='my_profile')],
        [InlineKeyboardButton("\U0001F517 اشتراک‌گذاری ربات", callback_data='share_bot')],
        [InlineKeyboardButton("\U0001F4B0 خرید اشتراک VIP", callback_data='buy_vip')],
        [InlineKeyboardButton("\U0001F310 افزودن ربات به گروه‌ها", callback_data='add_to_groups')],
        [InlineKeyboardButton("\U0001F4C8 دریافت سیگنال‌های معاملاتی", callback_data='daily_signals')],
        [InlineKeyboardButton("\U0001F570 زمان‌بندی جلسات", callback_data='session_timings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(welcome_message, reply_markup=reply_markup)

def handle_menu_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'crypto_prices':
        data = get_crypto_prices()
        query.edit_message_text(f"\U0001F4B8 {data}")
    elif query.data == 'gold_prices':
        data = get_gold_prices()
        query.edit_message_text(f"\U0001F947 {data}")
    elif query.data == 'forex_news':
        data = get_forex_news()
        query.edit_message_text(f"\U0001F4F0 {data}")
    elif query.data == 'my_profile':
        data = generate_profile(query.from_user)
        query.edit_message_text(f"\U0001F464 {data}")
    elif query.data == 'share_bot':
        data = "این ربات را با دوستان خود به اشتراک بگذارید: @candletory_bot"
        query.edit_message_text(f"\U0001F517 {data}")
    elif query.data == 'buy_vip':
        data = "برای خرید اشتراک VIP به این لینک مراجعه کنید: [اشتراک VIP](https://example.com)"
        query.edit_message_text(f"\U0001F4B0 {data}", parse_mode="Markdown")
    elif query.data == 'add_to_groups':
        data = "برای افزودن ربات به گروه خود از این لینک استفاده کنید: [افزودن ربات](https://t.me/candletory_bot?startgroup=new)"
        query.edit_message_text(f"\U0001F310 {data}", parse_mode="Markdown")
    elif query.data == 'daily_signals':
        data = "ویژگی سیگنال‌های روزانه به زودی فعال می‌شود!"
        query.edit_message_text(f"\U0001F4C8 {data}")
    elif query.data == 'session_timings':
        data = get_session_timings()
        query.edit_message_text(f"\U0001F570 {data}")

def get_crypto_prices():
    url = "https://studio.persianapi.com/api/general/crypto"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('data', 'داده‌ای یافت نشد!')
    except requests.RequestException as e:
        return f"خطا در دریافت قیمت ارز و کریپتو: {e}"

def get_gold_prices():
    url_gold = "https://studio.persianapi.com/api/gold"
    url_coin = "https://studio.persianapi.com/api/coin"
    try:
        gold_response = requests.get(url_gold)
        coin_response = requests.get(url_coin)
        gold_response.raise_for_status()
        coin_response.raise_for_status()
        gold_data = gold_response.json().get('data', 'داده‌ای یافت نشد!')
        coin_data = coin_response.json().get('data', 'داده‌ای یافت نشد!')
        return f"\U0001F947 طلا: {gold_data}\n\U0001F4B0 سکه: {coin_data}"
    except requests.RequestException as e:
        return f"خطا در دریافت قیمت طلا یا سکه: {e}"

def get_forex_news():
    url = "https://www.forexfactory.com/calendar"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='calendar__event-title')
        parsed_news = [item.get_text(strip=True) for item in news_items[:5]]
        return "\n".join(parsed_news) if parsed_news else "داده‌ای یافت نشد!"
    except requests.RequestException as e:
        return f"خطا در دریافت اخبار فارکس: {e}"
    except Exception as e:
        return f"خطای غیرمنتظره در پردازش اخبار فارکس: {e}"

def generate_profile(user):
    return (
        f"\U0001F464 پروفایل:\n"
        f"نام: {user.first_name} {user.last_name or ''}\n"
        f"نام کاربری: @{user.username}\n"
        f"امتیاز: 0 (با دعوت دوستان یا افزودن ربات به گروه‌ها امتیاز کسب کنید!)"
    )

def get_session_timings():
    iran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.datetime.now(iran_tz)
    return (
        f"\U0001F570 زمان‌بندی جلسات معاملاتی (به وقت ایران):\n"
        f"زمان فعلی: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        "- آسیا: 3:00 صبح - 12:00 ظهر\n"
        "- اروپا: 10:00 صبح - 6:30 عصر\n"
        "- آمریکا: 4:30 عصر - 1:00 بامداد"
    )

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_menu_selection))

    application.run_polling()

if __name__ == '__main__':
    main()