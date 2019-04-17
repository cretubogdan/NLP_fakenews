import csv
import os
from Logger import *

class Reader:
    ENV_PATH_DATASET_TRAIN_NAME = "DATASET_TRAIN_PATH"
    ENV_PATH_DATASET_TEST_NAME = "DATASET_TEST_PATH"

    path_train = None
    header_train = None
    body_train = []
    rows_train = 0
    filetype_train = None
    path_test = None
    header_test = None
    body_test = []
    rows_test = 0
    filetype_test = None
    logger = Logger()

    def __init__(self):
        if None == Reader.path_train:
            try:
                Reader.path_train = os.environ[Reader.ENV_PATH_DATASET_TRAIN_NAME]
                Reader.filetype_train = Reader.path_train.rsplit(".", 1)[1].lower()
                Reader.logger.Log(Severity.INFO, "Reader module initialization succesfully for the path_train: {0}".format(Reader.path_train))
                Reader.logger.Log(Severity.INFO, "File type_train is {0}".format(Reader.filetype_train))
            except:
                Reader.logger.Log(Severity.FATAL, "Environment variable {0} is not set".format(Reader.ENV_PATH_DATASET_TRAIN_NAME))

            try:
                Reader.path_test = os.environ[Reader.ENV_PATH_DATASET_TEST_NAME]
                Reader.filetype_test = Reader.path_test.rsplit(".", 1)[1].lower()
                Reader.logger.Log(Severity.INFO, "Reader module initialization succesfully for the path_test: {0}".format(Reader.path_test))
                Reader.logger.Log(Severity.INFO, "File type_test is {0}".format(Reader.filetype_test))
            except:
                Reader.logger.Log(Severity.FATAL, "Environment variable {0} is not set".format(Reader.ENV_PATH_DATASET_TEST_NAME))


    def Read(self):
        Reader.logger.Log(Severity.INFO, "Start reading file {0}".format(Reader.path_train))
        try:
            with open(Reader.path_train) as dataset:
                reader = None

                if Reader.filetype_train == "csv":
                    reader = csv.reader(dataset, delimiter = ",")
                elif Reader.filetype_train == "tsv":
                    reader = csv.reader(dataset, delimiter = "\t")

                for row in reader:
                    if Reader.rows_train == 0:
                        Reader.header_train = row
                    else:
                        Reader.body_train.append(row)
                    Reader.rows_train += 1

            Reader.logger.Log(Severity.INFO, "Finished reading file - {0} lines were read".format(Reader.rows_train - 1))
        except:
            Reader.logger.Log(Severity.ERROR, "Bad path for file - {0}".format(Reader.path_train))

        Reader.logger.Log(Severity.INFO, "Start reading file {0}".format(Reader.path_test))
        try:
            with open(Reader.path_test) as dataset:
                reader = None

                if Reader.filetype_test == "csv":
                    reader = csv.reader(dataset, delimiter = ",")
                elif Reader.filetype_test == "tsv":
                    reader = csv.reader(dataset, delimiter = "\t")

                for row in reader:
                    if Reader.rows_test == 0:
                        Reader.header_test = row
                    else:
                        Reader.body_test.append(row)
                    Reader.rows_test += 1

            Reader.logger.Log(Severity.INFO, "Finished reading file - {0} lines were read".format(Reader.rows_test - 1))
        except:
            Reader.logger.Log(Severity.WARNING, "Bad path for file - {0}".format(Reader.path_test))

    def GetHeaderTrain(self):
        return Reader.header_train

    def GetBodyTrain(self):
        return Reader.body_train

    def GetCountTrain(self):
        return Reader.rows_train - 1

    def GetHeaderTest(self):
        return Reader.header_test

    def GetBodyTest(self):
        return Reader.body_test

    def GetCountTest(self):
        return Reader.rows_test - 1


