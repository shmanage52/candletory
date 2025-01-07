from telethon import TelegramClient, events, Button
import requests
import json

# اطلاعات توکن ربات و مقداردهی اولیه
API_ID = 25709855  # عدد API_ID شما
API_HASH = '740efc27f273ac589176b85853ef8088'
BOT_TOKEN = '7575235119:AAGFR15l6OFkOq_8S05WXfTvoRuu4YCf0vQ'

# ایجاد کلاینت تلگرام
bot = TelegramClient('candletory_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# پیام خوشامد
WELCOME_MSG = """
👋 خوش آمدید به ربات CandleTory!
لطفاً یکی از گزینه‌های زیر را انتخاب کنید:
"""

# هندلر برای پیام‌های ورودی
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    # دکمه‌های شیشه‌ای
    buttons = [
        [Button.inline('📈 قیمت لحظه‌ای ارز و بازار کریپتو', b'crypto_prices')],
        [Button.inline('💰 قیمت طلا و سکه', b'gold_prices')],
        [Button.inline('📰 اخبار مهم دنیای فارکس', b'forex_news')],
        [Button.inline('👤 اطلاعات پروفایل من', b'profile')],
        [Button.inline('📤 اشتراک ربات با دوستان', b'share')],
        [Button.inline('✨ خرید اشتراک VIP', b'buy_vip')],
        [Button.inline('➕ اضافه کردن ربات به گروه‌ها', b'add_to_group')],
        [Button.inline('📊 درخواست سیگنال معاملاتی', b'daily_signals')],
        [Button.inline('⏰ زمان باز بودن بازارها', b'market_sessions')],
    ]
    await event.respond(WELCOME_MSG, buttons=buttons)

# هندلر برای دکمه‌ها
@bot.on(events.CallbackQuery)
async def callback(event):
    # دریافت داده دکمه
    data = event.data.decode('utf-8')
    
    if data == 'crypto_prices':
        await event.answer("در حال دریافت قیمت‌ها ...")
        response = requests.get('https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency_v2.json')
        if response.status_code == 200:
            prices = response.json()
            crypto_text = "\n".join([f"{item['title']}: {item['price']}" for item in prices.get('crypto', [])])
            await event.edit(f"💹 قیمت لحظه‌ای بازار کریپتو:\n\n{crypto_text}")
        else:
            await event.edit("خطا در دریافت اطلاعات قیمت کریپتو. لطفاً دوباره تلاش کنید.")
    
    elif data == 'gold_prices':
        await event.answer("در حال دریافت قیمت‌ها ...")
        response = requests.get('https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency_v2.json')
        if response.status_code == 200:
            prices = response.json()
            gold_text = "\n".join([f"{item['title']}: {item['price']}" for item in prices.get('gold', [])])
            await event.edit(f"💰 قیمت لحظه‌ای طلا و سکه:\n\n{gold_text}")
        else:
            await event.edit("خطا در دریافت اطلاعات قیمت طلا. لطفاً دوباره تلاش کنید.")
    
    elif data == 'profile':
        user_id = event.sender_id
        await event.edit(f"👤 اطلاعات پروفایل شما:\n\n🆔 ID: {user_id}\n🏆 امتیاز: 0\n✨ اشتراک VIP: فعال نیست")
    
    elif data == 'buy_vip':
        await event.edit("✨ برای خرید اشتراک VIP، لطفاً به این لینک مراجعه کنید: [لینک پرداخت](https://example.com)", link_preview=False)
    
    elif data == 'share':
        await event.edit("📤 ربات را با دوستان خود به اشتراک بگذارید:\nhttps://t.me/candletory_bot")
    
    elif data == 'add_to_group':
        await event.edit("➕ برای اضافه کردن ربات به گروه، از لینک زیر استفاده کنید:\nhttps://t.me/candletory_bot?startgroup=true")
    
    elif data == 'daily_signals':
        await event.edit("📊 سیگنال‌های روزانه به زودی فعال می‌شود. لطفاً در کانال ما عضو شوید.")
    
    elif data == 'market_sessions':
        await event.edit("⏰ زمان باز بودن بازارها:\n\n📈 فارکس: 24 ساعت (روزهای کاری)\n💰 طلا و ارز: 09:00 تا 17:00")
    
    else:
        await event.answer("❌ دستور نامعتبر.")

# اجرای ربات
print("ربات با موفقیت راه‌اندازی شد!")
bot.run_until_disconnected()