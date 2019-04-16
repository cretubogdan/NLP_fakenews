import csv
import os
from Logger import *

class Reader:
    ENV_PATH_DATASET_NAME = "DATASET_PATH"

    path = None
    header = None
    body = []
    rows = 0
    logger = Logger()
    filetype = None

    def __init__(self):
        if None == Reader.path:
            try:
                Reader.path = os.environ[Reader.ENV_PATH_DATASET_NAME]
                Reader.filetype = Reader.path.rsplit(".", 1)[1].lower()
                Reader.logger.Log(Severity.INFO, "Reader module initialization succesfully for the path: {0}".format(Reader.path))
                Reader.logger.Log(Severity.INFO, "File type is {0}".format(Reader.filetype))
            except:
                Reader.logger.Log(Severity.FATAL, "Environment variable {0} is not set".format(Reader.ENV_PATH_DATASET_NAME))


    def Read(self):
        Reader.logger.Log(Severity.INFO, "Start reading file")

        with open(Reader.path) as dataset:
            reader = None

            if Reader.filetype == "csv":
                reader = csv.reader(dataset, delimiter = ",")
            elif Reader.filetype == "tsv":
                reader = csv.reader(dataset, delimiter = "\t")

            for row in reader:
                if Reader.rows == 0:
                    Reader.header = row
                else:
                    Reader.body.append(row)
                Reader.rows += 1

        Reader.logger.Log(Severity.INFO, "Finished reading file - {0} lines were read".format(Reader.rows - 1))

    def GetHeader(self):
        return Reader.header

    def GetBody(self):
        return Reader.body

    def GetCount(self):
        return Reader.rows - 1
