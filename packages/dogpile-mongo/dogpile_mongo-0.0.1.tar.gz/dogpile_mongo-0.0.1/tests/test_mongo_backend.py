import unittest
from unittest import TestCase
from mongomock import MongoClient
from dogpile.cache import make_region


class TestMongoBacked(TestCase):

    @unittest.SkipTest
    def test_basic(self):
        db = MongoClient()['test']
        region = make_region().configure(
            'mongo',
            # arguments are same as mongo backend.
            arguments={
                'db': db,
            }
        )
        region.set("test", "value")
        region.set_multi({"key1": "value1", "key2": 100})
        print(region.get("test"))
        print(region.get_multi(["key1", "key2"]))
        print(region.get_multi(["key2", "key1"]))
