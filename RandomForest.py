import sys
sys.path.insert(0, 'modules')
from Logger import *
from DBManager import *
from WorkPool import *
from Reader import *

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords
import nltk
import pickle
import re

ID = 0
TITLE = 1
AUTHOR = 2
TEXT = 3
LABEL = 4
NAME = "name"
DATA = "data"

estimators = 10000 #debug
stop_words = None

vectorizer = None
data_features = None
forest = None
loaded_model = None

collection_dump_models = "models_dump"
dump_name = "randomforest_fake-news"

l = Logger()
wp = WorkPool()
r = Reader()
db = DBManager()

def do_init():
    global l, stop_words, collection_dump_models
    l.log(Severity.INFO, "Random forest: started init")
    stop_words = set(stopwords.words('english'))
    db.drop(collection_dump_models)
    l.log(Severity.INFO, "Random forest: finished init")

def do_read():
    global l, r
    l.log(Severity.INFO, "Random forest: started reading")
    r.read()
    #r.train = r.train[0:90] #debug
    #r.test = r.test[0:10] #debug
    l.log(Severity.INFO, "Random forest: finished reading")

@wp.do_tasks
def do_clean_helper(data):
    for d in data:
        d[TEXT] = re.sub("[^a-zA-Z]"," ", d[TEXT]).lower().split()
        words = [w for w in d[TEXT] if not w in stop_words]
        d[TEXT] = " ".join(words)

def do_clean():
    global l, r
    l.log(Severity.INFO, "Random forest: started cleaning")
    do_clean_helper(r.train)
    do_clean_helper(r.test)
    l.log(Severity.INFO, "Random forest: finished cleaning")

@wp.do_tasks
def get_text(data):
    to_return = []
    for d in data:
        to_return.append(d[TEXT])
    return to_return

@wp.do_tasks
def get_polarity(data):
    to_return = []
    for d in data:
        to_return.append(d[LABEL])
    return to_return


def do_dict():
    global l, data_features, r, vectorizer
    l.log(Severity.INFO, "Random forest: started creating dict")
    vectorizer = CountVectorizer()
    column_text = get_text(r.train)
    data_features = vectorizer.fit_transform(column_text).toarray()
    l.log(Severity.INFO, "Random forest: finished creating dict")

def do_train():
    global l, forest, r, estimators
    l.log(Severity.INFO, "Random forest: started train")
    forest = RandomForestClassifier(n_estimators = estimators)
    data_labels = get_polarity(r.train)
    forest = forest.fit(data_features, data_labels)
    l.log(Severity.INFO, "Random forest: finished traing")

def do_save():
    global l, forest, collection_dump_models, dump_name
    l.log(Severity.INFO, "Started saving model to db")
    tmp = pickle.dumps(forest)
    data = {NAME : dump_name, DATA : tmp}
    db.insert(data, collection_dump_models)
    l.log(Severity.INFO, "Finished saving model to db")

def do_load():
    global l, loaded_model
    l.log(Severity.INFO, "Started loading model from db")
    query = {NAME : dump_name}
    model = db.find(query, collection_dump_models)[0]
    loaded_model = pickle.loads(model[DATA])
    l.log(Severity.INFO, "Finished loading model from db")

def get_prediction_percent(predict, real):
    global l
    value = len([i for i, j in zip(predict, real) if i == j])
    value = float(value * 100 / len(predict))
    l.log(Severity.RESULT, "Random forest: predict percent: {0}".format(value))

def do_test():
    global l, r, vectorizer, loaded_model
    l.log(Severity.INFO, "Random forest: started testing")
    column_text = get_text(r.test)
    test_labels = get_polarity(r.test)
    test_features = vectorizer.transform(column_text).toarray()
    results = loaded_model.predict(test_features)
    get_prediction_percent(list(results), test_labels)
    l.log(Severity.INFO, "Random forest: finished testing")

def main():
    do_init()
    do_read()
    do_clean()
    do_dict()
    do_train()
    do_save()
    do_load()
    do_test()

if __name__ == '__main__':
    main()
    wp.abort()