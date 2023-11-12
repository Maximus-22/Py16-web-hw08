import json
from datetime import datetime

import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='hw-08 Events message', exchange_type='fanout')


def create_event():
    message = {
        'event': 'Test event',
        'message': "Test message",
        'detail': f"Date: {datetime.now().isoformat()}"
    }

    channel.basic_publish(exchange='hw-08 Events message', routing_key='', body=json.dumps(message).encode())

    connection.close()


if __name__ == '__main__':
    create_event()
