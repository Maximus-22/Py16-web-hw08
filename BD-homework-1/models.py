from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE


connect(db = "BD-homework",
        host = "mongodb+srv://maximusm_22:<password>@cluster0.aemcehc.mongodb.net/?retryWrites=true&w=majority",)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=20))
    quote = StringField()
    meta = {"collection": "quotes"}

    # Owerwrite the special method
    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)
