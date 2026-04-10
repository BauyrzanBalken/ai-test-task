import requests
from supabase import create_client
import json

# --- ТВОИ ДАННЫЕ ---
CRM_URL = 'https://bauyrzhanbalken.retailcrm.ru'
CRM_KEY = 'ugzVlBKbnnCOCi5UiObKoioqliqNwKv7'

SUPABASE_URL = 'https://sidmyoefdtbkdyvptzrs.supabase.co'
SUPABASE_KEY = 'sb_publishable_1zG_xgcdFaDc8DDXtL2eoA_u7PB0Z21'

TG_TOKEN = '8560866588:AAFWvZas6ui8toKrH9Jecgmfg8TeCP6u5f0'
TG_CHAT_ID = '5381966086' # Твое числовое ID
# -------------------

# Подключаемся к Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    response = requests.post(url, data={'chat_id': TG_CHAT_ID, 'text': text})
    if response.status_code != 200:
        print(f"❌ Ошибка отправки в TG: {response.text}")
    else:
        print(f"✅ Уведомление доставлено в Telegram!")
def sync():
    # 1. Получаем заказы из CRM
    url = f"{CRM_URL}/api/v5/orders?apiKey={CRM_KEY}&limit=100"
    response = requests.get(url)
    orders = response.json().get('orders', [])

    print(f"Синхронизирую {len(orders)} заказов...")

    for o in orders:
        order_id = o.get('id')
        first_name = o.get('firstName', 'Клиент')
        total_sum = float(o.get('totalSumm', 0))

        # 2. Сохраняем в Supabase (upsert - обновить если есть, создать если нет)
        data = {
            "order_id": order_id,
            "first_name": first_name,
            "total_sum": total_sum
        }
        
        try:
            supabase.table("orders").upsert(data, on_conflict="order_id").execute()
        except Exception as e:
            print(f"Ошибка Supabase: {e}")

        # 3. Условие на Телеграм (Шаг 5 задания)
        if total_sum > 50000:
            msg = f"💰 Крупный заказ! #{order_id}\nИмя: {first_name}\nСумма: {total_sum} ₸"
            send_telegram(msg)
            print(f"Отправил уведомление о заказе {order_id}")

    print("Синхронизация завершена!")

if __name__ == "__main__":
    sync()