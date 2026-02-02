import telebot
from telebot.types import ChatPermissions
import json
import time

TOKEN = "8576622508:AAFo1_gSxs4aH9NmCyktNdcq2DaInZf9xHk"
bot = telebot.TeleBot(TOKEN)

# So‘kinishlar ro‘yxati (o‘zingiz to‘ldirasiz)
BAD_WORDS = ["qse", "pashol", "idin", "onangni","kot","jalla","jalap", "dalbayob","dalbayop", "skey", "yiban","chumo", "idin", " idinaxuy", "idinnaxuy","xaromi", "sky", "om", "ominga", "qotagim" , "qq", "q.q","gandon","pedaraz","seks","kayf", "tashoq","kut","tashshoq"," qsee", "qqbosh"," iflos", "isqirt"
"yebsan" ]
WARNINGS_FILE = "warnings.json"

# Ogohlantirishlarni yuklash
def load_warnings():
    try:
        with open(WARNINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Saqlash
def save_warnings(data):
    with open(WARNINGS_FILE, "w") as f:
        json.dump(data, f)

warnings = load_warnings()

def contains_bad_word(text):
    text = text.lower()
    return any(word in text for word in BAD_WORDS)

@bot.message_handler(func=lambda message: True)
def check_message(message):
    if not message.text:
        return

    if contains_bad_word(message.text):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

        user_id = str(message.from_user.id)
        warnings[user_id] = warnings.get(user_id, 0) + 1
        save_warnings(warnings)

        count = warnings[user_id]

        if count < 3:
            bot.send_message(
                message.chat.id,
                f"⚠️ {message.from_user.first_name}, guruhda so‘kinmang!\nOgohlantirish: {count}/3"
            )
        else:
            # 1 soat mute
            until = int(time.time()) + 3600
            bot.restrict_chat_member(
                message.chat.id,
                message.from_user.id,
                ChatPermissions(can_send_messages=False),
                until_date=until
            )

            bot.send_message(
                message.chat.id,
                f"🚫 {message.from_user.first_name} 1 soatga yozishdan chetlatildi (ko‘p so‘kingani uchun)."
            )

print("Bot ishlayapti...")
bot.infinity_polling()

import re

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-zа-я0-9ўқғҳё]', '', text)  # belgilarni olib tashlash
    return text

def contains_bad_word(text):
    clean = normalize(text)
    return any(word in clean for word in BAD_WORDS)
    
    warnings[user_id] = {
    "count": 1,
    "last_time": time.time()
}
now = time.time()
user_data = warnings.get(user_id, {"count": 0, "last_time": now})

# 24 soatdan oshgan bo‘lsa reset
if now - user_data["last_time"] > 86400:
    user_data["count"] = 0

user_data["count"] += 1
user_data["last_time"] = now
warnings[user_id] = user_data
save_warnings(warnings)

count = user_data["count"]
warn_msg = bot.send_message(message.chat.id, "⚠️ So‘kinmang!")
time.sleep(5)
bot.delete_message(message.chat.id, warn_msg.message_id)
