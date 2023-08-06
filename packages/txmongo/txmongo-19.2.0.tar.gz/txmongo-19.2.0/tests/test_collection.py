# Copyright 2012-2015 TxMongo Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test the collection module.
Based on pymongo driver's test_collection.py
"""

from __future__ import absolute_import, division
from pymongo import errors
from twisted.internet import defer
from twisted.trial import unittest
import txmongo
from txmongo import filter as qf
from txmongo.collection import Collection

mongo_host = "localhost"
mongo_port = 27017


def cmp(a, b):
    if not isinstance(a, b.__class__) or not isinstance(b, a.__class__):
        return -1
    return (a > b) - (a < b)


class TestIndexInfo(unittest.TestCase):

    timeout = 5

    @defer.inlineCallbacks
    def setUp(self):
        self.conn = yield txmongo.MongoConnection(mongo_host, mongo_port)
        self.db = self.conn.mydb
        self.coll = self.db.mycol

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.conn.drop_database(self.db)
        yield self.conn.disconnect()

    @defer.inlineCallbacks
    def test_collection(self):
        self.assertRaises(TypeError, Collection, self.db, 5)

        def make_col(base, name):
            return base[name]

        self.assertRaises(errors.InvalidName, make_col, self.db, "")
        self.assertRaises(errors.InvalidName, make_col, self.db, "te$t")
        self.assertRaises(errors.InvalidName, make_col, self.db, ".test")
        self.assertRaises(errors.InvalidName, make_col, self.db, "test.")
        self.assertRaises(errors.InvalidName, make_col, self.db, "tes..t")
        self.assertRaises(errors.InvalidName, make_col, self.db.test, "")
        self.assertRaises(errors.InvalidName, make_col, self.db.test, "te$t")
        self.assertRaises(errors.InvalidName, make_col, self.db.test, ".test")
        self.assertRaises(errors.InvalidName, make_col, self.db.test, "test.")
        self.assertRaises(errors.InvalidName, make_col, self.db.test, "tes..t")
        self.assertRaises(errors.InvalidName, make_col, self.db.test, "tes\x00t")
        self.assertRaises(TypeError, self.coll.save, "test")
        self.assertRaises(ValueError, self.coll.filemd5, "test")
        self.assertRaises(TypeError, self.db.test.find, spec="test")
        self.assertRaises(TypeError, self.db.test.find, fields="test")
        self.assertRaises(TypeError, self.db.test.find, skip="test")
        self.assertRaises(TypeError, self.db.test.find, limit="test")
        self.assertRaises(TypeError, self.db.test.insert, [1])
        self.assertRaises(TypeError, self.db.test.insert, 1)
        self.assertRaises(TypeError, self.db.test.update, 1, 1)
        self.assertRaises(TypeError, self.db.test.update, {}, 1)
        self.assertRaises(TypeError, self.db.test.update, {}, {}, 'a')

        self.assert_(isinstance(self.db.test, Collection))
        self.assertEqual(NotImplemented, self.db.test.__cmp__(7))
        self.assertNotEqual(cmp(self.db.test, 7), 0)
        self.assertEqual(self.db.test, Collection(self.db, "test"))
        self.assertEqual(self.db.test.mike, self.db["test.mike"])
        self.assertEqual(self.db.test["mike"], self.db["test.mike"])
        self.assertEqual(repr(self.db.test), "Collection(mydb, test)")
        self.assertEqual(self.db.test.test, self.db.test("test"))

        options = yield self.db.test.options()
        self.assertTrue(isinstance(options, dict))

        yield self.db.drop_collection("test")
        collection_names = yield self.db.collection_names()
        self.assertFalse("test" in collection_names)

    @defer.inlineCallbacks
    def test_create_index(self):
        coll = self.coll

        self.assertRaises(TypeError, coll.create_index, 5)
        self.assertRaises(TypeError, coll.create_index, {"hello": 1})

        yield coll.insert({'c': 1})  # make sure collection exists.

        yield coll.drop_indexes()
        count = len((yield coll.index_information()))
        self.assertEqual(count, 1)
        self.assertIsInstance(count, int)

        yield coll.create_index(qf.sort(qf.ASCENDING("hello")))
        yield coll.create_index(qf.sort(qf.ASCENDING("hello") +
                                qf.DESCENDING("world")))

        count = len((yield coll.index_information()))
        self.assertEqual(count, 3)

        yield coll.drop_indexes()
        ix = yield coll.create_index(qf.sort(qf.ASCENDING("hello") +
                                     qf.DESCENDING("world")), name="hello_world")
        self.assertEquals(ix, "hello_world")

        yield coll.drop_indexes()
        count = len((yield coll.index_information()))
        self.assertEqual(count, 1)

        yield coll.create_index(qf.sort(qf.ASCENDING("hello")))
        indices = yield coll.index_information()
        self.assert_(u"hello_1" in indices)

        yield coll.drop_indexes()
        count = len((yield coll.index_information()))
        self.assertEqual(count, 1)

        ix = yield coll.create_index(qf.sort(qf.ASCENDING("hello") +
                                     qf.DESCENDING("world")))
        self.assertEquals(ix, "hello_1_world_-1")

    @defer.inlineCallbacks
    def test_create_index_nodup(self):
        coll = self.coll

        yield coll.insert({'b': 1})
        yield coll.insert({'b': 1})

        ix = coll.create_index(qf.sort(qf.ASCENDING("b")), unique=True)
        yield self.assertFailure(ix, errors.DuplicateKeyError)

    @defer.inlineCallbacks
    def test_create_index_dropdups(self):
        # dropDups was removed from MongoDB v3.0
        ismaster = yield self.db.command("ismaster")
        if ismaster["maxWireVersion"] >= 3:
            raise unittest.SkipTest("dropDups was removed from MongoDB 3")

        yield self.coll.insert([{'b': 1}, {'b': 1}])

        yield self.coll.create_index(qf.sort(qf.ASCENDING('b')),
                                          unique=True, drop_dups=True)
        docs = yield self.coll.find(fields={"_id": 0})
        self.assertEqual(docs, [{'b': 1}])

    @defer.inlineCallbacks
    def test_ensure_index(self):
        coll = self.coll

        yield coll.ensure_index(qf.sort(qf.ASCENDING("hello")))
        indices = yield coll.index_information()
        self.assert_(u"hello_1" in indices)

    @defer.inlineCallbacks
    def test_index_info(self):
        db = self.db

        db.test.save({})  # create collection
        ix_info = yield db.test.index_information()
        self.assertEqual(len(ix_info), 1)
        self.assertEqual(ix_info["_id_"]["name"], "_id_")

        yield db.test.create_index(qf.sort(qf.ASCENDING("hello")))
        ix_info = yield db.test.index_information()
        self.assertEqual(len(ix_info), 2)
        self.assertEqual(ix_info["hello_1"]["name"], "hello_1")

        yield db.test.create_index(
            qf.sort(qf.DESCENDING("hello") + qf.ASCENDING("world")),
            unique=True, sparse=True)
        ix_info = yield db.test.index_information()
        self.assertEqual(ix_info["hello_1"]["name"], "hello_1")
        self.assertEqual(len(ix_info), 3)
        self.assertEqual({"hello": -1, "world": 1}, ix_info["hello_-1_world_1"]["key"])
        self.assertEqual(True, ix_info["hello_-1_world_1"]["unique"])
        self.assertEqual(True, ix_info["hello_-1_world_1"]["sparse"])

    @defer.inlineCallbacks
    def test_index_geo2d(self):
        coll = self.coll
        geo_ix = yield coll.create_index(qf.sort(qf.GEO2D("loc")))

        self.assertEqual("loc_2d", geo_ix)

        index_info = yield coll.index_information()
        self.assertEqual({"loc": "2d"}, index_info["loc_2d"]["key"])

    @defer.inlineCallbacks
    def test_index_geo2dsphere(self):
        coll = self.coll
        geo_ix = yield coll.create_index(qf.sort(qf.GEO2DSPHERE("loc")))

        self.assertEqual("loc_2dsphere", geo_ix)
        index_info = yield coll.index_information()

        self.assertEqual(index_info["loc_2dsphere"]["key"], {"loc": "2dsphere"})

    @defer.inlineCallbacks
    def test_index_text(self):
        ix = yield self.coll.create_index(qf.sort(qf.TEXT("title") + qf.TEXT("summary")),
                                          weights={"title": 100, "summary": 20})
        self.assertEqual("title_text_summary_text", ix)

        index_info = yield self.coll.index_information()
        self.assertEqual(index_info[ix]["key"], {"_fts": "text", "_ftsx": 1})
        self.assertEqual(index_info[ix]["weights"], {"title": 100, "summary": 20})

    @defer.inlineCallbacks
    def test_index_haystack(self):
        db = self.db
        coll = self.coll

        _id = yield coll.insert({
            "pos": {"long": 34.2, "lat": 33.3},
            "type": "restaurant"
        })
        yield coll.insert({
            "pos": {"long": 34.2, "lat": 37.3}, "type": "restaurant"
        })
        yield coll.insert({
            "pos": {"long": 59.1, "lat": 87.2}, "type": "office"
        })

        yield coll.create_index(qf.sort(qf.GEOHAYSTACK("pos") +
                                        qf.ASCENDING("type")), **{"bucket_size": 1})

        results = yield db.command("geoSearch", "mycol",
                                   near=[33, 33],
                                   maxDistance=6,
                                   search={"type": "restaurant"},
                                   limit=30)

        self.assertEqual(2, len(results["results"]))
        self.assertEqual({
            "_id": _id,
            "pos": {"long": 34.2, "lat": 33.3},
            "type": "restaurant"
        }, results["results"][0])

    @defer.inlineCallbacks
    def test_drop_index(self):
        index = qf.sort(qf.ASCENDING("hello") + qf.DESCENDING("world"))

        yield self.coll.create_index(index, name="myindex")
        res = yield self.coll.drop_index("myindex")
        self.assertEqual(res["ok"], 1)

        yield self.coll.create_index(index)
        res = yield self.coll.drop_index(index)
        self.assertEqual(res["ok"], 1)

        self.assertRaises(TypeError, self.coll.drop_index, 123)


class TestRename(unittest.TestCase):

    def setUp(self):
        self.conn = txmongo.MongoConnection(mongo_host, mongo_port)
        self.db = self.conn.mydb

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.conn.drop_database(self.db)
        yield self.conn.disconnect()

    @defer.inlineCallbacks
    def test_Rename(self):
        coll = yield self.db.create_collection("coll1")
        yield coll.insert({'x': 42}, safe=True)

        yield coll.rename("coll2")

        doc = yield self.db.coll2.find_one(fields={"_id": 0})
        self.assertEqual(doc, {'x': 42})


class TestOptions(unittest.TestCase):

    def setUp(self):
        self.conn = txmongo.MongoConnection(mongo_host, mongo_port)
        self.db = self.conn.mydb

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.conn.drop_database(self.db)
        yield self.conn.disconnect()

    @defer.inlineCallbacks
    def test_Options(self):
        coll = yield self.db.create_collection("opttest", {"capped": True, "size": 4096})
        self.assertTrue(isinstance(coll, Collection))

        opts = yield coll.options()
        self.assertEqual(opts["capped"], True)
        self.assertEqual(opts["size"], 4096)

    @defer.inlineCallbacks
    def test_NonExistingCollection(self):
        opts = yield self.db.nonexisting.options()
        self.assertEqual(opts, {})

    @defer.inlineCallbacks
    def test_WithoutOptions(self):
        coll = yield self.db.create_collection("opttest")
        opts = yield coll.options()
        self.assertEqual(opts, {})


class TestCreateCollection(unittest.TestCase):

    def setUp(self):
        self.conn = txmongo.MongoConnection(mongo_host, mongo_port)
        self.db = self.conn.mydb

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.conn.drop_database(self.db)
        yield self.conn.disconnect()

    @defer.inlineCallbacks
    def test_WithOptions(self):
        coll = yield self.db.create_collection("opttest", capped=True, size=4096)
        self.assertTrue(isinstance(coll, Collection))

        opts = yield coll.options()
        self.assertEqual(opts["capped"], True)
        self.assertEqual(opts["size"], 4096)

    @defer.inlineCallbacks
    def test_Fail(self):
        # Not using assertFailure() here because it doesn't wait until deferred is
        # resolved or failed but there was a bug that made deferred hang forever
        # in case if create_collection failed
        try:
            # Negative size
            yield self.db.create_collection("opttest", {"size": -100})
        except errors.OperationFailure:
            pass
        else:
            self.fail()
    test_Fail.timeout = 10


class TestFindSignatureCompat(unittest.TestCase):
    def test_convert(self):
        self.assertEqual(
            Collection._find_args_compat(spec={'x': 42}),
            {"filter": {'x': 42}, "projection": None, "skip": 0, "limit": 0, "sort": None,
             "cursor": False}
        )
        self.assertEqual(
            Collection._find_args_compat(filter={'x': 42}),
            {"filter": {'x': 42}, "projection": None, "skip": 0, "limit": 0, "sort": None}
        )
        self.assertEqual(
            Collection._find_args_compat(filter=qf.sort(qf.ASCENDING('x'))),
            {"filter": None, "projection": None, "skip": 0, "limit": 0,
             "sort": qf.sort(qf.ASCENDING('x')), "cursor": False}
        )
        self.assertEqual(
            Collection._find_args_compat(sort=qf.sort(qf.ASCENDING('x'))),
            {"filter": None, "projection": None, "skip": 0, "limit": 0,
             "sort": qf.sort(qf.ASCENDING('x'))}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}),
            {"filter": {'x': 42}, "projection": None, "skip": 0, "limit": 0, "sort": None}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, unknown_arg=123),
            {"filter": {'x': 42}, "projection": None, "skip": 0, "limit": 0, "sort": None,
             "unknown_arg": 123}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, {'a': 1}),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 0, "limit": 0, "sort": None}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, projection={'a': 1}),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 0, "limit": 0, "sort": None}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, fields={'a': 1}),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 0, "limit": 0, "sort": None,
             "cursor": False}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, 5),
            {"filter": {'x': 42}, "projection": None, "skip": 5, "limit": 0, "sort": None,
             "cursor": False}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, {'a': 1}, 5),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 5, "limit": 0, "sort": None}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, {'a': 1}, 5, 6),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 5, "limit": 6, "sort": None}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, 5, 6, {'a': 1}),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 5, "limit": 6, "sort": None,
             "cursor": False}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, {'a': 1}, 5, 6, qf.sort([('s', 1)])),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 5, "limit": 6,
             "sort": qf.sort([('s', 1)])}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, 5, 6, {'a': 1}, qf.sort([('s', 1)])),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 5, "limit": 6,
             "sort": qf.sort([('s', 1)]), "cursor": False}
        )
        self.assertEqual(
            Collection._find_args_compat({'x': 42}, 5, 6, {'a': 1}, qf.sort([('s', 1)]), True),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 5, "limit": 6,
             "sort": qf.sort([('s', 1)]), "cursor": True}
        )
        self.assertEqual(
            Collection._find_args_compat(spec={'x': 42}, filter=qf.sort([('s', 1)]), limit=6,
                                         fields={'a': 1}, skip=5),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 5, "limit": 6,
             "sort": qf.sort([('s', 1)]), "cursor": False}
        )
        self.assertEqual(
            Collection._find_args_compat(filter={'x': 42}, sort=qf.sort([('s', 1)]), limit=6,
                                         projection={'a': 1}, skip=5),
            {"filter": {'x': 42}, "projection": {'a': 1}, "skip": 5, "limit": 6,
             "sort": qf.sort([('s', 1)])}
        )
