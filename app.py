import os
import requests
from woocommerce import API
from dotenv import load_dotenv
from datetime import timedelta, datetime, time

load_dotenv()

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

def get_message():
    COSTUMER_KEY = os.getenv('COSTUMER_KEY')
    COSTUMER_SECRET = os.getenv('COSTUMER_SECRET')
    wcapi = API(
        url="http://larpradeda.com.ua",
        consumer_key=COSTUMER_KEY,
        consumer_secret=COSTUMER_SECRET,
        version="wc/v3"
    )
    allOrders = wcapi.get("orders").json()
    dateToday = datetime.today()
    dateYestoday = dateToday - timedelta(days=1)
    datetime_last_order = datetime.strptime(allOrders[0]["date_created_gmt"], '%Y-%m-%dT%H:%M:%S')
    newOrders = []
    msg = ''
    if (dateYestoday > datetime_last_order):
        msg = 'Новых заказов нет'
    else:
        i = 0
        while(dateYestoday < datetime.strptime(allOrders[i]["date_created_gmt"], '%Y-%m-%dT%H:%M:%S')):
            newOrders.append(allOrders[i]["id"])
            i += 1
            if (i > 9):
                msg = '10 новых заказав. А может даже больше'
                break
        orders = ' '.join(str(e) for e in newOrders)
        msg = f"Новых заказов - {i} шт. ({orders})"
    return msg


if __name__ == '__main__':
    msg = get_message()
    send_message(msg)
