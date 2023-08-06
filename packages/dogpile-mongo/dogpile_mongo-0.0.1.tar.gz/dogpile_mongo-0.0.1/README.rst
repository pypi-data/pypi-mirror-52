==========================
dogpile_mongo
==========================

Install
=======

Use pip::

   pip install dogpile_mongo

Usage
=====

See the example.

Code::

   from dogpile.cache import make_region

   db = MongoClient()['test']
   region = make_region().configure(
        'mongo',
        # arguments are same as mongo backend.
        arguments={
            'db': db,
        }
   )

   region.set("test", b"value")
   region.set_multi({"key1": b"value1", "key2": 100})
   print(region.get("test"))
   print(region.get_multi(["key1", "key2"]))

Result::

   $ python main.py
   b'value'
   [b'value1', b'100']


