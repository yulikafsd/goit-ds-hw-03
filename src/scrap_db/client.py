from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://yulikafsd:123123123@goit-ds-hw.6o502ui.mongodb.net/?retryWrites=true&w=majority&appName=goit-ds-hw",
    server_api=ServerApi("1"),
)

db = client.test