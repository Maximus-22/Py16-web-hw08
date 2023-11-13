import pika
import json
import time

from mongoengine import connect, Document, BooleanField, StringField
from bson import ObjectId

from models import connect, Contact


CONSUMER = "Maximus"

# Подключение к MongoDB
connect(db="BD-homework", host="mongodb+srv://maximusm_22:<password>@cluster0.aemcehc.mongodb.net/?retryWrites=true&w=majority")

class Contact(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(required=True, max_length=64) 
    email = StringField(required=True)
    completed = BooleanField(default=False)
    consumer = StringField(max_length=64)
    meta = {"collection": "contacts"}

# Функция-заглушка для имитации отправки электронных писем
def send_email(contact_id):
    time.sleep(1.5)
    print(f"Sending email to contact with ID: {contact_id}")
    # Здесь можно добавить реальную логику отправки электронного письма

# Функция обработки сообщения из RabbitMQ
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')

    # Получение контакта по ID
    contact = Contact.objects.get(id=contact_id, completed=False)
    if contact:
        # Имитация отправки электронного письма
        send_email(contact_id)

        # Установка поля completed в True
        contact.completed = True
        contact.consumer = CONSUMER
        contact.save()

        print(f"Processed message for contact with ID: {contact_id} - successfully.")
        ch.basic_ack(delivery_tag=method.delivery_tag)

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='contact_queue')

# Установка обработчика сообщений
channel.basic_consume(queue='contact_queue', on_message_callback=callback, auto_ack=False)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()