import telebot
import sqlite3
import re

TOKEN = "توکن_ربات_خودت"  # توکن دریافتی از BotFather
bot = telebot.TeleBot(TOKEN)

# تابع برای ذخیره پیام‌های دارای هشتگ
def save_message(chat_id, message_id, text):
    hashtags = re.findall(r"#\w+", text)
    if not hashtags:
        return

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO messages (chat_id, message_id, text, hashtags) VALUES (?, ?, ?, ?)", 
                   (chat_id, message_id, text, ",".join(hashtags)))
    
    conn.commit()
    conn.close()

# دریافت و ذخیره پیام‌ها
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text:
        save_message(message.chat.id, message.message_id, message.text)

    # بررسی اگر پیام فقط شامل یک هشتگ برای جستجو باشد
    if message.text.strip().startswith("#"):
        hashtag = message.text.strip()
        conn = sqlite3.connect("messages.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT text FROM messages WHERE hashtags LIKE ?", ('%' + hashtag + '%',))
        results = cursor.fetchall()
        
        conn.close()
        
        if results:
            response = "\n\n".join([row[0] for row in results])
        else:
            response = "هیچ پیامی با این هشتگ یافت نشد!"
        
        bot.send_message(message.chat.id, response)

# اجرای ربات
print("ربات فعال شد...")
bot.polling()
