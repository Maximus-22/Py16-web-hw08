import json
from datetime import datetime

import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='hw-08 exchange', exchange_type='direct')
channel.queue_declare(queue='hw-08_queue', durable=True)
channel.queue_bind(exchange='hw-08 exchange', queue='hw-08_queue')


def create_tasks(nums: int):
    for i in range(nums):
        message = {
            'id': i + 1,
            'payload': f"Date: {datetime.now().isoformat()}"
        }

        channel.basic_publish(exchange='hw-08 exchange', routing_key='hw-08_queue', body=json.dumps(message).encode())

    connection.close()


if __name__ == '__main__':
    create_tasks(100)
