from pymongo import MongoClient
from Logger import *
from threading import Lock

class DbManager:
    host = 'localhost'
    port = 27017
    lock = Lock()
    client = None

    def __init__(self):
        logger = Logger()
        DbManager.lock.acquire()

        if None == DbManager.client:
            try:
                client = MongoClient(DbManager.host, DbManager.port)
                logger.Log(Severity.INFO, "Successfully connected to the DB: {0}:{1}".format(DbManager.host, DbManager.port))
            except:
                logger.Log(Severity.FATAL, "Couldn't connect to the DB: {0}:{1}".format(DbManager.host, DbManager.port))

        DbManager.lock.release()
