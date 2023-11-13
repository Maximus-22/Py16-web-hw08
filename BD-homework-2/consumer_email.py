import pika
import json
import time

from mongoengine import connect, Document, BooleanField, StringField
from bson import ObjectId

from models import connect, Contact


CONSUMER = "Freddy"


# Функція-заглушка для імітації надсилання електронних листів
def send_email(contact_id):
    time.sleep(2)
    print(f"Sending E-mail to contact with ID: {contact_id}")
    # Здесь можно добавить реальную логику отправки электронного письма

# Функція обробки повідомлення з RabbitMQ
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')

    # Отримання контакту за ID
    contact = Contact.objects.get(id=contact_id, completed=False)
    if contact:
        # Імітація надсилання електронного листа
        send_email(contact_id)

        # Встановлення поля completed у True
        contact.completed = True
        contact.consumer = CONSUMER
        contact.save()

        print(f"Processed message for contact with ID: {contact_id} - successfully.")
        ch.basic_ack(delivery_tag=method.delivery_tag)


# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення обмінника [exchange] із типом <direct>
channel.exchange_declare(exchange='contact_exchange', exchange_type='direct')

# Визначення черг для email та sms
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

# Прив'язка черг до обмінника з використанням маршрутизації за ключем
channel.queue_bind(exchange='contact_exchange', queue='email_queue', routing_key='email')
channel.queue_bind(exchange='contact_exchange', queue='sms_queue', routing_key='sms')

# Підключення обробника повідомлень (1 consumer = 1 queue)
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=False)
# channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=False)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()