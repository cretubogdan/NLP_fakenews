from threading import RLock
import os
import time
from enum import Enum
import sys

class Severity(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4

class Logger:
    ENV_VAR_PATH_NAME = 'LOGGER_PATH'
    DO_DEBUG = 'DEBUG'
    file = None
    lock = RLock()
    do_debug = True

    def __init__(self):
        Logger.lock.acquire()

        if None == Logger.file:
            try:
                Logger.do_debug = (os.environ[Logger.DO_DEBUG] == "TRUE")
            except:
                pass

            error = 0
            try:
                path = os.environ[Logger.ENV_VAR_PATH_NAME]
                Logger.file = open(path, 'a+')
                self.Log(Severity.INFO, "Logger initialization succesfully at the path: {0}".format(path))
            except:
                error = 1
            
            if 1 == error:
                try:
                    path = os.getcwd()
                    path += '/logs'
                    file = open(path, 'a+')
                    self.Log(Severity.WARNING, "Env variable {0} was not set. Trying to write in current directory".format(Logger.ENV_VAR_PATH_NAME))
                    self.Log(Severity.INFO, "Logger initialization succesfully at the path: {0}".format(path))
                except:
                    error = 2

            if 2 == error:
                Logger.file = sys.stdout
                self.Log(Severity.WARNING, "Error writting in the current directory: {0}".format(path))
                self.Log(Severity.WARNING, "Logger initialization succesfully at the STDOUT")
        
        Logger.lock.release()

    @staticmethod
    def TimeNow():
        return time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())

    def Log(self, level, message):
        Logger.lock.acquire()
        if Logger.do_debug == True or level != Severity.INFO:
            Logger.file.write("[{0}]:[{1}]:{2}\n".format(Logger.TimeNow(), level.name, message))
        Logger.lock.release()

    def Close(self):
        Logger.file.close()
