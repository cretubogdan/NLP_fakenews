import sys
sys.path.insert(0, '../modules')
from Logger import *
from DBManager import *
from WorkPool import *
from Reader import *

from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pickle

POLARITY = 0
ID = 1
DATE = 2
QUERY = 3
USER = 4
TEXT = 5

MIN_DF = 5
MAX_DF = 0.8

l = Logger()
wp = WorkPool()
r = Reader()
db = DBManager()

collection_dump_models = "models_dump_svm_sa"

vectorizer = TfidfVectorizer(min_df = MIN_DF, max_df = MAX_DF, use_idf = True)
tf_idf = None
model_trained = None
model_loaded = None

def do_init():
    l.log(Severity.INFO, "Started init")
    l.log(Severity.INFO, "Finished init")

def do_read():
    l.log(Severity.INFO, "Started reading")
    r.read()
    r.train = r.train[0:100] #debug
    r.test = r.test[0:100] #debug
    l.log(Severity.INFO, "Finished reading")

@wp.do_tasks
def do_clean_helper(data):
    for d in data:
        d[TEXT] = d[TEXT].lower()

def do_clean():
    l.log(Severity.INFO, "Started cleaning")
    do_clean_helper(r.train)
    do_clean_helper(r.test)
    l.log(Severity.INFO, "Finished cleaning")

@wp.do_tasks
def get_text(data):
    to_return = []
    for d in data:
        to_return.append(d[TEXT])
    return to_return

@wp.do_tasks
def get_labels(data):
    to_return = []
    for d in data:
        to_return.append(d[POLARITY])
    return to_return

def do_features():
    global tf_idf
    l.log(Severity.INFO, "Started creating features")
    train = get_text(r.train)
    tf_idf = vectorizer.fit_transform(train)
    l.log(Severity.INFO, "Finished creating features")

def do_train():
    global tf_idf, model_trained
    l.log(Severity.INFO, "Started train")
    labels = get_labels(r.train)
    model_trained = svm.SVC()
    model_trained.fit(tf_idf, labels)
    l.log(Severity.INFO, "Finished traing")

def do_save():
    global model_trained
    l.log(Severity.INFO, "Started saving model to db")
    dump = pickle.dumps(model_trained)
    db.grid_insert(dump, collection_dump_models)
    l.log(Severity.INFO, "Finished saving model to db")

def do_load():
    global model_loaded
    l.log(Severity.INFO, "Started loading model from db")
    model = db.grid_find(collection_dump_models)
    model_loaded = pickle.loads(model)
    l.log(Severity.INFO, "Finished loading model from db")

def get_prediction_percent(predict, real):
    value = len([i for i, j in zip(predict, real) if i == j])
    value = float(value * 100 / len(predict))
    l.log(Severity.RESULT, "Predict percent: {0}".format(value))

def do_test():
    global model_loaded
    l.log(Severity.INFO, "Started testing")
    test = get_text(r.test)
    labels = get_labels(r.test)
    test_tf_idf = vectorizer.transform(test)
    results = model_loaded.predict(test_tf_idf)
    get_prediction_percent(results, labels)
    l.log(Severity.INFO, "Finished testing")

def main():
    do_init()
    do_read()
    do_clean()
    do_features()
    do_train()
    do_save()
    do_load()
    do_test()

if __name__ == '__main__':
    main()
    wp.abort()