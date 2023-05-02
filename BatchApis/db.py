from pymongo import MongoClient

import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

# For JD Database
def jdclient():
    client = MongoClient(MONGO_URI)
    db = client["DjangoDB"]
    collection = db["JobDesc"]

    return collection

# For search index Database
def data_db(field_name):
    client = MongoClient(MONGO_URI)
    db = client["DjangoDB"]
    collection = db[field_name]

    return collection