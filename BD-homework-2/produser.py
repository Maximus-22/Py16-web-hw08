from mongoengine import connect, Document, BooleanField, StringField
from bson import ObjectId
import pika
import json
import random

from faker import Faker

from models import connect, Contact


NUM_CONTACTS = 8


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


# Генерація випадкових типизованих даних із використанням Faker
def generate_fake_contact():
    fake = Faker('uk_UA')
    contact_data = {
        "fullname": fake.name(),
        "born_date": fake.date_of_birth().strftime("%Y-%m-%d"),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "delivery_method": random.choice(["email", "sms"]),
    }
    return contact_data


# Генерація документів колекції та запис їх до бази даних
def generate_contacts(num_contacts):
    contacts_ids = []
    for _ in range(num_contacts):
        contact_data = generate_fake_contact()
        contact = Contact(**contact_data).save()
        contacts_ids.append(str(contact.id))
    return contacts_ids


# Надсилання ObjectID у чергу RabbitMQ
def send_to_rabbitmq(contact_ids):
    for contact_id in contact_ids:
        contact = Contact.objects.get(id=contact_id, completed=False)
        if contact.delivery_method == "email":
            queue_name = 'email_queue'
        elif contact.delivery_method == "sms":
            queue_name = 'sms_queue'
        else:
            print(f"Invalid delivery method for contact with ID: {contact_id}")
            continue
        message = {"contact_id": contact_id}
        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
        print(f"Sent message with contact_id: {contact_id}")


if __name__ == "__main__":
    # Генерація документів колекції та відправлення ObjectID у RabbitMQ
    contacts_ids = generate_contacts(NUM_CONTACTS)
    send_to_rabbitmq(contacts_ids)

    # Закриття з'єднань
    connection.close()