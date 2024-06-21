from random import randint, sample
from faker import Faker
from client import db

fake = Faker(["uk_UA", "it_IT", "es_ES", "en_US"])

cat_features = [
    "хижий",
    "гуляє сам по собі",
    "граційний",
    "витончений",
    "робить те, що хоче",
    "любить свободу",
    "прив’язується до господаря",
    "чутливий",
    "відчуває настрій",
    "грайливий",
    "спокійний",
    "витримує обійми",
    "галасує ночами",
    "вередливий",
    "пухнастий",
    "не любить гратись",
    "любить дітей",
    "бойовий",
    "розумний",
    "великий",
    "добродушний",
    "має милі складочки",
    "має великі вушка",
    "ходить на лоток",
    "чухається",
    "дере диван",
    "ходить в капці",
    "дає себе гладити",
    "рудий",
]


cats_list = []


# Generate features for a cat
def generate_features():
    features_list = sample(cat_features, randint(1, 5))
    return features_list


# Create cat docs <num> times
def create_cats(num):
    for _ in range(num):
        cats_list.append(
            {
                "name": fake.first_name(),
                "age": randint(0, 15),
                "features": generate_features(),
            }
        )
    return cats_list


# Insert cat docs into the collection and show the new docs
def insert_cats(num):
    db.cats.insert_many(create_cats(num))
    cat_docs = list(db.cats.find().sort([("_id", -1)]).limit(num))
    for cat_doc in cat_docs:
        print(cat_doc)


if __name__ == "__main__":
    insert_cats(10)
