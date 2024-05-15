import os
import requests
from woocommerce import API
from dotenv import load_dotenv

load_dotenv()

def saveOrdersInFile(data=''):
    with open('orders.txt', "w") as file:
        if data == '':
            orders = get_orders()
            file.write(orders)
        else:
            file.write(data)


def compareOrders(orders):
    if not os.path.exists('orders.txt'):
        saveOrdersInFile()
    lastOrders = []
    message = ''
    with open("orders.txt", "r") as fp:
        lastOrders = fp.read().split()
    orders = orders.split()
    if orders[0] != lastOrders[0]:
        for idx, order in enumerate(orders):
            if order == lastOrders[0]:
                message = f'Есть новые заказы: {orders[0:idx]}'
                break
            else:
                message = f'У тебя 10 заказов!!! Работай!!!'
        orders = " ".join(orders)
        saveOrdersInFile(orders)
    else:
        message = 'Новых заказов нет'
    return message

def get_orders():
    COSTUMER_KEY = os.getenv('COSTUMER_KEY')
    COSTUMER_SECRET = os.getenv('COSTUMER_SECRET')
    wcapi = API(
        url="http://larpradeda.com.ua",
        consumer_key=COSTUMER_KEY,
        consumer_secret=COSTUMER_SECRET,
        version="wc/v3"
    )
    allOrders = wcapi.get("orders").json()
    ids = []
    for order in allOrders:
        ids.append(order['id'])
    return " ".join(map(str,ids))

def send_message(message):
    TELEGRAM_TOCKEN = os.getenv('TELEGRAM_TOCKEN')
    TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    url = f'https://api.telegram.org/bot{TELEGRAM_TOCKEN}/sendMessage'
    params = {
        'chat_id': TELEGRAM_CHANNEL_ID,
        'text': message
        }
    res = requests.post(url, params=params)
    res.raise_for_status() #В случае ошибки, в консоль выведет её
    return res.json()

if __name__ == '__main__':
    orders = get_orders()
    mes = compareOrders(orders)
    send_message(mes)
