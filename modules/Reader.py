import csv
import sys
import os
import random
from Logger import *

class Reader:
    ENV_VAR_DATASET = "DATASET"
    train_percent = 0.9

    path = None
    header = None
    body = []
    rows = 0
    filetype = None
    logger = Logger()

    train = []
    test = []

    def __init__(self):
        if None == Reader.path:
            try:
                csv.field_size_limit(sys.maxsize)
                Reader.path = os.environ[Reader.ENV_VAR_DATASET]
                Reader.filetype = Reader.path.rsplit(".", 1)[1].lower()
                Reader.logger.log(Severity.INFO, "Reader module initialization succesfully for the path_train: {0}".format(Reader.path))
                Reader.logger.log(Severity.INFO, "File type_train is {0}".format(Reader.filetype))
            except:
                Reader.logger.log(Severity.FATAL, "Environment variable {0} is not set".format(Reader.ENV_VAR_DATASET))

    def read(self):
        Reader.logger.log(Severity.INFO, "Start reading file {0}".format(Reader.path))
        
        try:
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
            Reader.rows -= 1

            Reader.logger.log(Severity.INFO, "Finished reading file {0} lines were read".format(Reader.rows))
        except:
            Reader.logger.log(Severity.ERROR, "Bad path for file {0}".format(Reader.path))

        random.shuffle(Reader.body)
        Reader.train = Reader.body[0:int(Reader.train_percent * Reader.rows)]
        Reader.test = Reader.body[int(Reader.train_percent * Reader.rows):Reader.rows]