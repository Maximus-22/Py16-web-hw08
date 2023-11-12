import pickle

import redis

client = redis.Redis(host='localhost', port=6379, password=None)

if __name__ == '__main__':
    client.set("username1", "Artem")
    client.set("username2", "Natalia")
    client.expire("username1", 600)

    client.set("count", 100)

    n = client.get("count")
    # результат -> завжди бiнарний рядок, тобто потрiбно використовувати переведення типiв
    print(int(n))

    # у якостi параметру можна використовувати тiльки рядок, або бiнарний рядок, тож тут нам дуже
    # знадобиться [pickle]
    client.set("test_list", pickle.dumps([2, 3, 4]))
    test_list = pickle.loads(client.get("test_list"))
    print(test_list)
