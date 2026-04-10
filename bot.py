import telebot
from supabase import create_client
import json

# --- НАСТРОЙКИ ---
TOKEN = '8560866588:AAFWvZas6ui8toKrH9Jecgmfg8TeCP6u5f0'
SUPABASE_URL = 'https://sidmyoefdtbkdyvptzrs.supabase.co'
SUPABASE_KEY = 'sb_publishable_1zG_xgcdFaDc8DDXtL2eoA_u7PB0Z21'

bot = telebot.TeleBot(TOKEN)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("📊 Статистика")
    btn2 = telebot.types.KeyboardButton("💰 Последние заказы")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привет! Я твой CRM-ассистент. Выбери действие:", reply_markup=markup)

# Обработка кнопки "Статистика"
@bot.message_handler(func=lambda message: message.text == "📊 Статистика")
def get_stats(message):
    # Запрос в Supabase для подсчета суммы
    response = supabase.table("orders").select("total_sum").execute()
    orders = response.data
    
    if orders:
        total_count = len(orders)
        total_amount = sum(item['total_sum'] for item in orders)
        bot.send_message(message.chat.id, f"📈 **Общая статистика:**\n\nВсего заказов: {total_count}\nНа сумму: {total_amount:,.0f} ₸")
    else:
        bot.send_message(message.chat.id, "Заказов пока нет в базе.")

# Обработка кнопки "Последние заказы"
@bot.message_handler(func=lambda message: message.text == "💰 Последние заказы")
def get_recent(message):
    response = supabase.table("orders").select("*").order("created_at", desc=True).limit(5).execute()
    orders = response.data
    
    if orders:
        text = "🔔 **Последние 5 заказов:**\n\n"
        for o in orders:
            text += f"ID: {o['order_id']} | {o['first_name']} | {o['total_sum']} ₸\n"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "Заказов нет.")

print("Бот запущен...")
bot.polling(none_stop=True)