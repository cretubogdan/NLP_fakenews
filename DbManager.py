from pymongo import MongoClient
from Logger import *
from threading import Lock

class DbManager:
    host = 'localhost'
    port = 27017
    db_name = 'SA'
    lock = Lock()
    client = None
    db = None
    col = None
    col_name = None
    logger = Logger()

    def __init__(self, col_name):
        DbManager.lock.acquire()

        if None == DbManager.client:
            try:
                DbManager.client = MongoClient(DbManager.host, DbManager.port)
                DbManager.db = DbManager.client[db_name]
                DbManager.col = DbManager.db[col_name]
                DbManager.col_name = col_name
                DbManager.logger.Log(Severity.INFO, "Successfully connected to the DB: {0}:{1}".format(DbManager.host, DbManager.port))
            except:
                DbManager.logger.Log(Severity.FATAL, "Couldn't connect to the DB: {0}:{1}".format(DbManager.host, DbManager.port))

        DbManager.lock.release()


    def Insert(value):
        try:
            DbManager.col.insert_one(value)
            DbManager.logger.Log(Severity.INFO, "New insert into the DB: {0}:{1}".format(db_name, col_name))
        except:
            DbManager.logger.Log(Severity.ERROR, "Something went wrong, couldn't insert into the DB: {0}:{1}".format(db_name, col_name))

    def InsertBulk(values):
        try:
            DbManager.col.insert_many(values)
            DbManager.logger.Log(Severity.INFO, "New bulk insert into the DB: {0}:{1}".format(db_name, col_name))
        except:
            DbManager.logger.Log(Severity.ERROR, "Something went wrong, couldn't bulk insert into the DB: {0}:{1}".format(db_name, col_name))

    def Delete(value):
        try:
            DbManager.col.delete_one(value)
            DbManager.logger.Log(Severity.INFO, "New delete from DB: {0}:{1}".format(db_name, col_name))
        except:
            DbManager.logger.Log(Severity.ERROR, "Couldn't delete data from DB: {0}:{1}".format(db_name, col_name))

    def DeleteBulk(values):
        try:
            DbManager.col.delete_many(values)
            DbManager.logger.Log(Severity.INFO, "New bulk delete from DB: {0}:{1}".format(db_name, col_name))
        except:
            DbManager.logger.Log(Severity.ERROR, "Couldn't bulk delete data from DB: {0}:{1}".format(db_name, col_name))

    def Update(condition, values):
        try:
            DbManager.col.update_one(condition, values)
            DbManager.logger.Log(Severity.INFO, "New update into the DB: {0}:{1}".format(db_name, col_name))
        except:
            DbManager.logger.Log(Severity.ERROR, "Couldn't update data into the DB: {0}:{1}".format(db_name, col_name))

    def UpdateBulk(condition, values):
        try:
            DbManager.col.update_many(condition, values)
            DbManager.logger.Log(Severity.INFO, "New bulk update into the DB: {0}:{1}".format(db_name, col_name))
        except:
            DbManager.logger.Log(Severity.ERROR, "Couldn't bulk update data into the DB: {0}:{1}".format(db_name, col_name))

    def Find(condition):
        try:
            DbManager.col.find(condition)
            DbManager.logger.Log(Severity.INFO, "New find into the DB: {0}:{1}".format(db_name, col_name))
        except:
            DbManager.logger.Log(Severity.ERROR, "Error while trying to find into the DB: {0}:{1}".format(db_name, col_name))

    def NewCol(col_name):
        DbManager.col_name = col_name
        DbManager.col = DbManager.db[col_name]
        DbManager.logger.log(Severity.INFO, "Collection switched to {0} for DB: {1}".format(col_name, db_name))

    def DropCol():
        try:
            DbManager.col.drop()
            DbManager.logger.Log(Severity.INFO, "Collection: {0} dropped succesfully".format(col_name))
        except:
            DbManager.logger.Log(Severity.ERROR, "Collection: {0} couldn't be drop".format(col_name))
