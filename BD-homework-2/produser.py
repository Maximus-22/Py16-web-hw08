from mongoengine import connect, Document, BooleanField, StringField
from bson import ObjectId
import pika
import json
from faker import Faker


NUM_CONTACTS = 5

# Подключение к MongoDB
connect(db="BD-homework", host="mongodb+srv://maximusm_22:<password>@cluster0.aemcehc.mongodb.net/?retryWrites=true&w=majority")

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='contact_queue')

class Contact(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(required=True, max_length=64) 
    email = StringField(required=True)
    completed = BooleanField(default=False)
    consumer = StringField(max_length=64)
    meta = {"collection": "contacts"}

# Генерация случайных данных с использованием Faker
def generate_fake_contact():
    fake = Faker('uk_UA')
    contact_data = {
        "fullname": fake.name(),
        "born_date": fake.date_of_birth().strftime("%Y-%m-%d"),
        "email": fake.email(),
    }
    return contact_data

# Генерация контактов и запись в базу данных
def generate_contacts(num_contacts):
    contacts_ids = []
    for _ in range(num_contacts):
        contact_data = generate_fake_contact()
        contact = Contact(**contact_data).save()
        contacts_ids.append(str(contact.id))
    return contacts_ids

# Отправка ObjectID в очередь RabbitMQ
def send_to_rabbitmq(contact_ids):
    for contact_id in contact_ids:
        message = {"contact_id": contact_id}
        channel.basic_publish(exchange='',
                              routing_key='contact_queue',
                              body=json.dumps(message))
        print(f"Sent message with contact_id: {contact_id}")

# Генерация контактов и отправка ObjectID в RabbitMQ
if __name__ == "__main__":
    contacts_ids = generate_contacts(NUM_CONTACTS)
    send_to_rabbitmq(contacts_ids)

    # Закрытие соединений
    connection.close()