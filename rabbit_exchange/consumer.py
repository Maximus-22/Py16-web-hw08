import json
import os
import sys
import time

import pika


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='hw-08_queue', durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f" [x] Received {message}")
        time.sleep(1.5)
        # Кожнiй задачi в чергi надається унiкальний параметр <delivery_tag>.
        print(f" [x] Completed {method.delivery_tag} task")
        # Функцiя [callback()] отримає змiнну [ch], щоб можна було вiдповiдати Produser.
        # Тут функцiя [callback()] говорить Produser, що завдання <method.delivery_tag> виконане.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hw-08_queue', on_message_callback=callback) # Увага! Тут пiдставлена сигнатура функцiї!!

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
