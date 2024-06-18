from random import randint
from faker import Faker
from client import db

fake = Faker(["it_IT", "es_ES", "en_US"])

cats_list = []


def generate_features():
    features_list = []
    for _ in range(randint(1, 5)):
        features_list.append(" ".join(fake.words(randint(1, 4))))
    return features_list


for _ in range(10):
    cats_list.append(
        {
            "name": fake.first_name(),
            "age": randint(0, 15),
            "features": generate_features(),
        }
    )


db.cats.insert_many(cats_list)
