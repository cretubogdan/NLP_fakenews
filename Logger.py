from __future__ import with_statement
from threading import Lock
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
    file = None
    lock = Lock()

    def __init__(self):
        with Logger.lock:
            if None == Logger.file:
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
                        Logger.file = open(path, 'a+')
                        self.Log(Severity.WARNING, "Env variable {0} was not set. Trying to write in current directory".format(Logger.ENV_VAR_PATH_NAME))
                        self.Log(Severity.INFO, "Logger initialization succesfully at the path: {0}".format(path))
                    except:
                        error = 2

                if 2 == error:
                    Logger.file = sys.stdout
                    self.Log(Severity.WARNING, "Error writting in the current directory: {0}".format(path))
                    self.Log(Severity.WARNING, "Logger initialization succesfully at the STDOUT")

    @staticmethod
    def TimeNow():
        return time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())

    def Log(self, level, message):
        with Logger.lock:
            Logger.file.write("[{0}]:[{1}]:{2}\n".format(Logger.TimeNow(), level.name, message))
