from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# URI = "mongodb+srv://<username>:<password>@<clastername in Atlas from menu [Connect]>/<databasename>?retryWrites=true&w=majority"
uri = "mongodb+srv://maximusm_22:<password>@cluster0.aemcehc.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api = ServerApi("1"))

# Вибір бази даних
db = client["hw-08"]

try:
    # Вибір колекції всередині бази даних та використання [insert_many] для вставлення записів
    db.cats.insert_many(
        [
            {
                "name": "Boris",
                "age": 5,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Мурзик",
                "age": 2,
                "features": ["iнодi ходить в капцi", "дає себе гладити", "смугастий"],
            },
            {
                "name": "Inessa",
                "age": 7,
                "features": ["iнодi ригає на пiдлогу", "постiйно випадає шерсть", "чорна"],
            },
        ]
    )
except Exception as err:
    print(err)
