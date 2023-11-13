from mongoengine import connect, Document, BooleanField, StringField

connect(db="BD-homework",
    host="mongodb+srv://maximusm_22:<password>@cluster0.aemcehc.mongodb.net/?retryWrites=true&w=majority",)


class Contact(Document):
    fullname = StringField(required=True, unique=True, max_length=128)
    born_date = StringField(required=True, max_length=64) 
    email = StringField(required=True, max_length=64)
    phone_number = StringField(required=True, max_length=24)
    delivery_method = StringField(choices=["email", "sms"])
    completed = BooleanField(default=False)
    consumer = StringField(max_length=32)
    meta = {"collection": "contacts"}
