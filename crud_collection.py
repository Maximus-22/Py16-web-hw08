import argparse

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://maximusm_22:<password>@cluster0.aemcehc.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi("1"))
db = client["hw-08"]

parser = argparse.ArgumentParser(description="Server Cats Enterprise")
parser.add_argument("-a", "--action", help="create, read, update, delete")  # CRUD action
parser.add_argument("--id")
parser.add_argument("--name")
parser.add_argument("--age")
parser.add_argument("--features", nargs="+")

arg = vars(parser.parse_args())

action = arg.get("action")
primary_key = arg.get("id")
name = arg.get("name")
age = arg.get("age")
features = arg.get("features")


def find():
    return db.cats.find()


def create(name, age, features):
    rezlt = db.cats.insert_one(
        {
            "name": name,
            "age": age,
            "features": features,
        }
    )
    return rezlt


def update(primary_key, name, age, features):
    # У MongoDB функцiя [update] працює завжди, як замiна старого об'єкту на новий, тобто, якщо потрiбно
    # оновити тiльки одне поле в записi, то необхiдно повторити всi вже внесенi данi та атрибути цього запису
    # та додати змiннi данi
    # У даному випадку застосований оператор [$set], який вказує на те, що потрiбно тiлькi замiнити данi у
    # визначених полях.
    rezlt = db.cats.update_one(
        {"_id": ObjectId(primary_key)},
        {
            "$set": {
                "name": name,
                "age": age,
                "features": features,
            }
        },
    )
    return rezlt


def delete(primary_key):
    return db.cats.delete_one({"_id": ObjectId(primary_key)})


# У конспектi функцiя [delete] використовує [name]
# але, якщо з таким атрибутом багато записiв, передбачити який з них буде видалено неможливо...
def delete_by_name(name):
    return db.cats.delete_one({"name": name})


def main():
    match action:
        case "create":
            rezlt = create(name, age, features)
            print(rezlt)
        case "read":
            rezlt = find()
            print(*[elem for elem in rezlt], sep = "\n")
        case "update":
            rezlt = update(primary_key, name, age, features)
            print(rezlt)
        case "delete":
            rezlt = delete(primary_key)
            print(rezlt)
        case _:
            print("Unknown command")


if __name__ == "__main__":
    main()
