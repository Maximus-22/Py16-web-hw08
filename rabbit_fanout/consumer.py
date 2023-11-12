import json
import os
import sys
import time

import pika


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    # Черга порожня, бо ми її не создавали.
    # Тут у Observer для кожного Consumer своя унiкальна черга -> параметр <exclusive>.
    # Тобто наступний рядок -> нам потрiбна унiкальна черга для даного Consumer.
    q = channel.queue_declare(queue='', exclusive=True)
    # Нам потрiбно iм'я, яке сгенеровано для цiєї черги.
    name_q = q.method.queue
    # Бiндемось на боцi Consumer.
    channel.queue_bind(exchange='hw-08 Events message', queue=name_q)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f" [x] Received {message}")

    channel.basic_consume(queue=name_q, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
