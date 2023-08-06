from dogpile.cache.api import CacheBackend, CachedValue
from dogpile.cache.api import NO_VALUE
from pymongo import MongoClient

__all__ = 'MongoBackend',


class MongoBackend(CacheBackend):
    def __init__(self, arguments):
        self._db = arguments.pop("db")
        if not self._db:
            self._db = MongoClient(arguments.pop('uri'))[arguments.pop('db_name')]
        self._db_collection = arguments.pop('db_collection', '__cache__')

    def get(self, key):
        value = self._db[self._db_collection].find_one({'_id': key}) or NO_VALUE
        if value is not NO_VALUE:
            value = CachedValue(*value['value'])
        return value

    def get_multi(self, keys):
        if not keys:
            return []
        docs = self._db[self._db_collection].aggregate([
            {'$match': {'_id': {'$in': keys}}},
            {'$addFields': {'__order': {'$indexOfArray': [keys, '$_id']}}},
            {'$sort': {'__order': 1}}])
        return map(lambda d: CachedValue(*d['value']), docs)

    def set(self, key, value):
        self._db[self._db_collection].insert_one({'_id': key, 'value': value})

    def set_multi(self, mapping):
        self._db[self._db_collection].insert_many([{'_id': key, 'value': value} for key, value in mapping.items()])

    def delete(self, key):
        self._db[self._db_collection].delete_one({'_id': key})

    def delete_multi(self, keys):
        self._db[self._db_collection].delete_many({'_id': {'$in': keys}})
