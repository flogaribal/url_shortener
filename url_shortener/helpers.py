from .config import *
import datetime
from .constants import *
import random


class URLEntry:

    def __init__(self, url, name, short_url, date_created, expiry_date=None, dates_clicked=None, _id=None, extra_info=None):
        if dates_clicked is None:
            dates_clicked = []
        self._id = _id
        self.url = url
        self.name = name
        self.short_url = short_url
        self.expiry_date = expiry_date
        self.date_created = date_created
        self.dates_clicked = dates_clicked
        self.extra_info = extra_info

    def to_dict(self):
        return {
            "_id":              str(self._id),
            "url":              self.url,
            "name":             self.name,
            "short_url":        self.short_url,
            "date_created":     self.date_created.isoformat(),
            "expiry_date":      self.expiry_date.isoformat() if self.expiry_date is not None else None,
            "dates_clicked":    [date_clicked.isoformat() for date_clicked in self.dates_clicked],
            "extra_info":       self.extra_info
        }

    def to_mongo(self):
        return {
            "_id":              str(self._id),
            "url":              self.url,
            "name":             self.name,
            "short_url":        self.short_url,
            "date_created":     self.date_created,
            "expiry_date":      self.expiry_date,
            "dates_clicked":    [date_clicked for date_clicked in self.dates_clicked],
            "extra_info":       self.extra_info
        }
    
    def __str__(self):
        return f"{{_id: {self._id}, url: {self.url}, name:{self.name}, short_url: {self.short_url}, " \
               f"date_created: {self.date_created}, expiry_date: {self.expiry_date}," \
               f"dates_clicked: {self.dates_clicked}," \
               f"extra_info: {str(self.extra_info)}}}"


# URLEntry HANDLING
def url_entry_from_db_entry(db_entry):
    DEBUG and print(db_entry)
    extra_info = None
    if 'extra_info' in db_entry:
        extra_info = db_entry['extra_info']
    return URLEntry(
        db_entry['url'],
        db_entry['name'],
        db_entry['short_url'],
        db_entry['date_created'],
        db_entry['expiry_date'],
        db_entry['dates_clicked'],
        db_entry['_id'],
        extra_info)


def create_url_entry(url, name, expiry_date, extra_info, mongo_client, db_name,
                     collection_name, short_url_length, short_url_possible_characters):
    return URLEntry(url, name, generate_short_url(mongo_client, db_name, collection_name, short_url_length,
                                                  short_url_possible_characters), datetime.datetime.utcnow(),
                    expiry_date, extra_info=extra_info)


def generate_short_url(mongo_client, db_name, collection_name,
                       short_url_possible_characters, short_url_length):
    short_url = generate_random_string(short_url_length, short_url_possible_characters)
    while db_url_entry_exists(short_url, mongo_client, db_name, collection_name):
        short_url = generate_random_string(short_url_length, short_url_possible_characters)

    return short_url


# MONGO CONNECTIONS
def get_db(client, db):
    return client[db]


def get_collection(client, db, collection_name):
    return get_db(client, db)[collection_name]


# MONGO HANDLING
def insert_db_url_entry(url_entry, mongo_client, db_name, collection_name):
    collection = get_collection(mongo_client, db_name, collection_name)
    DEBUG and print(f"Inserting {url_entry}")
    url_entry_dict = url_entry.to_mongo()
    url_entry_dict.pop("_id")
    db_url_entry_id = collection.insert_one(url_entry_dict).inserted_id
    DEBUG and print(f"Inserted with ID {db_url_entry_id}")
    return url_entry_from_db_entry(collection.find_one({'_id': db_url_entry_id})).to_dict()


def db_url_entry_exists(short_url, mongo_client, db_name, collection_name):
    collection = get_collection(mongo_client, db_name, collection_name)
    cursor = collection.find({"short_url": short_url})
    return cursor.count() > 0


def db_url_entry_exists_with_collection(short_url, collection):
    cursor = collection.find({"short_url": short_url})
    return cursor.count() > 0


# RANDOM STRING GENERATION
def generate_random_string(length, possible_character_categories):
    return_string = ""

    for i in range(length):
        character_type = possible_character_categories[random.randint(0, len(possible_character_categories) - 1)]
        character = characters_map[character_type][random.randint(0, len(characters_map[character_type]) - 1)]
        return_string += character
    
    return return_string
