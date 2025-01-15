import asyncio
from telethon import TelegramClient, events, Button
import httpx  # Ensure httpx is imported
import logging  # Add logging import

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Bot token and initialization
API_ID = 25709855  # Your API_ID
API_HASH = '740efc27f273ac589176b85853ef8088'
BOT_TOKEN = '7575235119:AAGFR15l6OFkOq_8S05WXfTvoRuu4YCf0vQ'  # Replace with your actual bot token

# Create the Telegram client
bot = TelegramClient('candletory_bot', API_ID, API_HASH)

async def main():
    # Start the bot with the bot token
    await bot.start(bot_token=BOT_TOKEN)

    logging.debug("Bot started with token: %s", BOT_TOKEN)
    print("Bot is running...")

    # Welcome message
    WELCOME_MSG = """
    🤖 Hi, I'm Candletory Bot!
    ♦ Please select a Option below and explore my features.
    • Don't forget to add me to your groups! ♥️

    ✨ By the way...
    I love it when you invite your friends! 🥰
    """

    # Handler for incoming messages
    @bot.on(events.NewMessage(pattern='/start'))
    async def start(event):
        logging.debug("Received /start command from user: %s", event.sender_id)
        # Inline buttons
        buttons = [
            [Button.text('📈 قیمت لحظه‌ای ارز و بازار کریپتو')],
            [Button.text('💰 قیمت طلا و سکه')],
            [Button.text('💸 قیمت دلار و ارز')],
            [Button.text('👤 اطلاعات پروفایل من')],
            [Button.text('📤 اشتراک ربات با دوستان')],
            [Button.text('✨ خرید اشتراک VIP')],
            [Button.text('➕ اضافه کردن ربات به گروه‌ها')],
            [Button.text('📊 درخواست سیگنال معاملاتی')],
            [Button.text('⏰ زمان باز بودن بازارها')],
        ]
        await event.respond(WELCOME_MSG, buttons=buttons)

    # Handler for button presses
    @bot.on(events.NewMessage)
    async def handle_message(event):
        text = event.raw_text  # Text message sent by the user (button clicked name)
        logging.debug("Received message: %s from user: %s", text, event.sender_id)

        if text == '📈 قیمت لحظه‌ای ارز و بازار کریپتو':
            logging.debug("Fetching crypto prices")
            async with httpx.AsyncClient() as client:
                response = httpx.get('https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency_v2.json')
                if response.status_code == 200:
                    logging.debug("Crypto prices fetched successfully")
                    prices = response.json()
                    crypto_text = "\n".join([
                        f"{item['name']}: {item['price']} ({item['time']}) 📈 {item['change_percent']}%"
                        if item['change_percent'] > 0 else
                        f"{item['name']}: {item['price']} ({item['time']}) 📉 {item['change_percent']}%"
                        for item in prices.get('cryptocurrency', [])
                    ])
                    await event.reply(f"📈 قیمت لحظه‌ای ارز و بازار کریپتو:\n\n{crypto_text}")
                else:
                    logging.error("Failed to fetch crypto prices")
                    await event.reply("خطا در دریافت اطلاعات قیمت کریپتو.")
        
        elif text == '💰 قیمت طلا و سکه':
            logging.debug("Fetching gold prices")
            async with httpx.AsyncClient() as client:
                response = httpx.get('https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency_v2.json')
                if response.status_code == 200:
                    logging.debug("Gold prices fetched successfully")
                    prices = response.json()
                    gold_text = "\n".join([
                        f"{item['name']}: {item['price']} ({item['time']}) 📈 {item['change_percent']}%"
                        if item['change_percent'] > 0 else
                        f"{item['name']}: {item['price']} ({item['time']}) 📉 {item['change_percent']}%"
                        for item in prices.get('gold', [])
                    ])
                    await event.reply(f"💰 قیمت لحظه‌ای طلا و سکه:\n\n{gold_text}")
                else:
                    logging.error("Failed to fetch gold prices")
                    await event.reply("خطا در دریافت اطلاعات قیمت طلا.")
        
        elif text == '💸 قیمت دلار و ارز':
            logging.debug("Fetching currency prices")
            async with httpx.AsyncClient() as client:
                response = httpx.get('https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency_v2.json')
                if response.status_code == 200:
                    logging.debug("Currency prices fetched successfully")
                    prices = response.json()
                    currency_text = "\n".join([
                        f"{item['name']}: {item['price']} ({item['time']}) 📈 {item['change_percent']}%"
                        if item['change_percent'] > 0 else
                        f"{item['name']}: {item['price']} ({item['time']}) 📉 {item['change_percent']}%"
                        for item in prices.get('currency', [])
                    ])
                    await event.reply(f"💸 قیمت لحظه‌ای ارز:\n\n{currency_text}")
                else:
                    logging.error("Failed to fetch currency prices")
                    await event.reply("خطا در دریافت اطلاعات قیمت ارز.")
        
        elif text == '👤 اطلاعات پروفایل من':
            logging.debug("Fetching profile info for user: %s", event.sender_id)
            user_id = event.sender_id
            await event.reply(f"👤 اطلاعات پروفایل شما:\n\n🆔 ID: {user_id}\n🏆 امتیاز: 0\n✨ اشتراک VIP: فعال نیست")
        
        elif text == '📤 اشتراک ربات با دوستان':
            logging.debug("User %s wants to share the bot", event.sender_id)
            await event.reply("📤 ربات را با دوستان خود به اشتراک بگذارید:\nhttps://t.me/candletory_bot")
        
        elif text == '✨ خرید اشتراک VIP':
            logging.debug("User %s wants to buy VIP subscription", event.sender_id)
            await event.reply("✨ برای خرید اشتراک VIP، لطفاً به این لینک مراجعه کنید:\nhttps://example.com")
        
        elif text == '➕ اضافه کردن ربات به گروه‌ها':
            logging.debug("User %s wants to add the bot to groups", event.sender_id)
            await event.reply("➕ برای اضافه کردن ربات به گروه، از لینک زیر استفاده کنید:\n https://t.me/candletory_bot?startgroup=true")
        
        elif text == '📊 درخواست سیگنال معاملاتی':
            logging.debug("User %s requested trading signals", event.sender_id)
            await event.reply("📊 سیگنال‌های روزانه به زودی فعال می‌شود. لطفاً در کانال ما عضو شوید:\nhttps://t.me/candletory")
        
        elif text == '⏰ زمان باز بودن بازارها':
            logging.debug("User %s requested market open times", event.sender_id)
            await event.reply("⏰ زمان باز بودن بازارها:\n\n📈 فارکس: 24 ساعت (روزهای کاری)\n💰 طلا و ارز: 09:00 تا 17:00")
        
        else:
            logging.warning("User %s sent an invalid command: %s", event.sender_id, text)
            await event.reply("❌ دستور نامعتبر.")

    pass
    # Keep the bot running until it is disconnected
    await bot.run_until_disconnected()

if __name__ == "__main__":
    # Run the async main function inside an event loop
    bot.loop.run_until_complete(main())