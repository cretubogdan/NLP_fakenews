from pymongo import MongoClient
from Logger import *
from threading import Lock

class DBManager:
    host = 'localhost'
    port = 27017
    db_name = 'fake_news_sa'
    lock = Lock()
    client = None
    db = None
    l = Logger()

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
        DBManager.l.log(Severity.INFO, "New insert made under id <{0}> in collection <{1}> has been made".format(ret.inserted_id, collection_name))

    def find(self, query, collection_name):
        collection = DBManager.__get_collection(collection_name)
        ret = None
        if query is None:
            ret = collection.find()
        else:
            ret = collection.find(query)
        DBManager.l.log(Severity.INFO, "New find made in collection <{0}>".format(collection_name))
        return ret

    def delete(self, query, collection_name):
        collection = DBManager.__get_collection(collection_name)
        collection.delete_many(query)
        DBManager.l.log(Severity.INFO, "New delete made in collection <{0}>".format(collection_name))

    def drop(self, collection_name):
        collection = DBManager.__get_collection(collection_name)
        collection.drop()
        DBManager.l.log(Severity.INFO, "Collection <{0}> was dropped".format(collection_name))
