from pymongo import MongoClient
from Logger import *
from threading import Lock
import gridfs

class DBManager:
    host = 'localhost'
    port = 27017
    db_name = 'fake_news_sa'
    collection_name_dumps = "dumps"
    fs_chunks = "fs.chunks"
    fs_files = "fs.files"
    lock = Lock()
    client = None
    db = None
    l = Logger()

    ID = "ID"
    COLLECTION_NAME = "COLLECTION_NAME"
    
    def __init__(self):
        DBManager.lock.acquire()

        if None == DBManager.client:
            try:
                DBManager.client = MongoClient(DBManager.host, DBManager.port)
                DBManager.db = DBManager.client[DBManager.db_name]
                DBManager.l.log(Severity.INFO, "Successfully connected to the DB: {0}:{1}".format(DBManager.host, DBManager.port))
            except:
                DBManager.l.log(Severity.FATAL, "Couldn't connect to the DB: {0}:{1}".format(DBManager.host, DBManager.port))

        DBManager.lock.release()

    def __del__(self):
        self.close()

    def close(self):
        try:
            DBManager.logger.log(Severity.INFO, "Db connection will be closed")
            DBManager.client.close()
        except:
            pass

    @staticmethod
    def __get_collection(collection_name):
        return DBManager.db[collection_name]

    def insert(self, data, collection_name):
        collection = DBManager.__get_collection(collection_name)
        ret = collection.insert_one(data)
        DBManager.l.log(Severity.INFO, "New insert under id <{0}> in collection <{1}> has been made".format(ret.inserted_id, collection_name))

    def grid_insert(self, dump, collection_name):
        fs = gridfs.GridFS(DBManager.db)
        id = fs.put(dump)
        data = {DBManager.ID : id, DBManager.COLLECTION_NAME : collection_name}
        DBManager.l.log(Severity.INFO, "New insert made under id <{0}> in gridfs".format(id))
        self.insert(data, DBManager.collection_name_dumps)

    def find(self, query, collection_name):
        collection = DBManager.__get_collection(collection_name)
        ret = None
        if query is None:
            ret = collection.find()
        else:
            ret = collection.find(query)
        DBManager.l.log(Severity.INFO, "New find made in collection <{0}>".format(collection_name))
        return ret

    def find_2(self, query, collection_name):
        collection = DBManager.__get_collection(collection_name)
        ret = None
        if query is None:
            ret = collection.find()
        else:
            ret = collection.find({}, query)
        DBManager.l.log(Severity.INFO, "New find made in collection <{0}>".format(collection_name))
        return ret

    def grid_find(self, collection_name):
        ret = None
        id = None
        fs = gridfs.GridFS(DBManager.db)
        query = {DBManager.COLLECTION_NAME : collection_name}
        ids = self.find(query, DBManager.collection_name_dumps)
        for ids_elem in ids:
            id = ids_elem
        id = id[DBManager.ID]
        ret = fs.get(id).read()
        DBManager.l.log(Severity.INFO, "New find made in gridfs for id <{0}>".format(id))
        return ret

    def delete(self, query, collection_name):
        collection = DBManager.__get_collection(collection_name)
        collection.delete_many(query)
        DBManager.l.log(Severity.INFO, "New delete made in collection <{0}>".format(collection_name))

    def drop(self, collection_name):
        collection = DBManager.__get_collection(collection_name)
        collection.drop()
        DBManager.l.log(Severity.INFO, "Collection <{0}> was dropped".format(collection_name))

    def drop_dumps(self):
        self.drop(DBManager.collection_name_dumps)
        self.drop(DBManager.fs_chunks)
        self.drop(DBManager.fs_files)
