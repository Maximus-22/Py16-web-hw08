from typing import List, Any
import functools

import redis
# from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host = "localhost", port = 6379, password = None)
# cache = RedisLRU(client)


# @cache
# Максимальний розмiр кешу у кiлькостi об'єктiв [елементiв], потiм видалення бiльш старих
@functools.lru_cache(maxsize=128)
def find_by_tag(tag: str) -> list[str | None]:
    print(f"\nFind by {tag}")
    quotes = Quote.objects(tags__iregex = tag)
    result = [q.quote for q in quotes]
    return result


# @cache
# Максимальний розмiр кешу у кiлькостi об'єктiв [елементiв], потiм видалення бiльш старих
@functools.lru_cache(maxsize=64)
def find_by_author(author: str) -> list[list[Any]]:
    print(f"\nFind by {author}")
    authors = Author.objects(fullname__iregex = author)
    result = {}
    for auth in authors:
        quotes = Quote.objects(author = auth)
        result[auth.fullname] = [q.quote for q in quotes]
    return result


def main():
        while True:
            user_input = input("\nPlease, enter queries [command:value]\n(for example - \"name:Steve Martin\", \
\"tag:humor\", \"tags:life,world\", \"exit\"):\n")
            
            if user_input.lower() == "exit":
                print("\nExiting the program. By-by.")
                break
            
            parts = user_input.split(":")
            if len(parts) != 2:
                print("\nInvalid input format. Please use [command:value] format.")
                continue
            
            command, value = parts
            if command == "name":
                regex_value = f".*{value.strip()}.*"
                result = find_by_author(regex_value)
                print(f"\nSearch result by {value.strip()}:", result, sep = "\n")
            elif command == "tag":
                regex_value = f".*{value.strip()}.*"
                result = find_by_tag(regex_value)
                print(f"\nSearch result by {value.strip()}:", *result, sep = "\n")
            elif command == "tags":
                tags = [tag.strip() for tag in value.split(',')]
                result = []
                for tag in tags:
                    result.extend(find_by_tag(tag))
                print(f"\nSearch result by {tags}:", *result, sep = "\n")
            else:
                print("\nInvalid command. Supported commands: [name], [tag], [tags], [exit].")


if __name__ == '__main__':
    main()
    # print(find_by_tag('mi'))
    # print(find_by_tag('mi'))
    # print(find_by_author('in'))
    # print(find_by_author('in'))
    # quotes = Quote.objects().all()
    # print([e.to_json() for e in quotes])

