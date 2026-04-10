import json
import requests
import time

# Твои данные для подключения
API_KEY = 'ugzVlBKbnnCOCi5UiObKoioqliqNwKv7' # Не забудь кавычки!
BASE_URL = 'https://bauyrzhanbalken.retailcrm.ru'

def upload():
    # Открываем файл с заказами
    try:
        with open('mock_orders.json', 'r', encoding='utf-8') as f:
            orders = json.load(f)
    except FileNotFoundError:
        print("Ошибка: файл mock_orders.json не найден в этой папке!")
        return

    print(f"Нашел {len(orders)} заказов. Начинаю загрузку...")

    for i, order_data in enumerate(orders):
        url = f"{BASE_URL}/api/v5/orders/create"
        
        # Формируем запрос
        payload = {
            'apiKey': API_KEY,
            'order': json.dumps(order_data) # Превращаем данные заказа в строку
        }

        response = requests.post(url, data=payload)
        result = response.json()

        if result.get('success'):
            print(f"[{i+1}] Заказ для {order_data['firstName']} загружен!")
        else:
            print(f"Ошибка на заказе {i+1}: {result.get('errors')}")
        
        # Пауза полсекунды, чтобы не спамить
        time.sleep(0.5)

    print("\nВсё! Иди в RetailCRM и обновляй страницу с заказами.")

if __name__ == "__main__":
    upload()