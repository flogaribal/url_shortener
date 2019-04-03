from pymongo import ReturnDocument
from .helpers import *


class UrlShortener:

    def __init__(self, mongo_client, db_name, collection_name,
                 short_url_possible_characters, short_url_length):
        self.mongo_client = mongo_client
        self.db_name = db_name
        self.collection_name = collection_name
        self.short_url_possible_characters = short_url_possible_characters
        self.short_url_length = short_url_length

    def generate_and_insert_short_url(self, url, name, expiry_date=None, extra_info=None):
        url_entry = create_url_entry(url, name, expiry_date, extra_info, self.mongo_client, self.db_name,
                                     self.collection_name, self.short_url_possible_characters, self.short_url_length)
        return insert_db_url_entry(url_entry, self.mongo_client, self.db_name, self.collection_name)

    def get_db_url_entry(self, short_url):
        collection = get_collection(self.mongo_client, self.db_name, self.collection_name)
        if db_url_entry_exists_with_collection(short_url, collection):
            return url_entry_from_db_entry(collection.find_one({"short_url": short_url})).to_dict()
        else:
            return None

    def db_url_entry_exists(self, short_url):
        collection = get_collection(self.mongo_client, self.db_name, self.collection_name)
        return db_url_entry_exists_with_collection(short_url, collection)

    def get_all_db_url_entry(self):
        collection = get_collection(self.mongo_client, self.db_name, self.collection_name)
        all_urls = collection.find({})
        return [url_entry_from_db_entry(url).to_dict() for url in all_urls]

    def add_click_date(self, short_url):
        collection = get_collection(self.mongo_client, self.db_name, self.collection_name)
        if db_url_entry_exists_with_collection(short_url, collection):
            return collection.find_one_and_update({'short_url': short_url},
                                                  {'$push': {'dates_clicked': datetime.datetime.utcnow()}},
                                                  return_document=ReturnDocument.AFTER)
        else:
            return None

    def delete_db_url_entry(self, short_url):
        collection = get_collection(self.mongo_client, self.db_name, self.collection_name)
        if db_url_entry_exists_with_collection(short_url, collection):
            return collection.delete_one({'short_url': short_url})
        else:
            return None

    def get_all_categories(self):
        db = get_db(self.mongo_client, self.db_name)
        return db.list_collection_names()
