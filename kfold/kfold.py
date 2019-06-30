import sys
sys.path.insert(0, '../modules')
import os
import csv
from Logger import *
#from DBManager import *
from WorkPool import *
#from Reader import *

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from nltk.corpus import stopwords
import nltk
import pickle
import re
import concurrent.futures

l = Logger()
wp = WorkPool()

dataset_sa = []
dataset_fn = []

vectorizer = TfidfVectorizer(min_df=5, max_df=0.8, use_idf=True)

@wp.do_tasks
def get_text(data):
    to_return = []
    for d in data:
        to_return.append(d[0])
    return to_return

@wp.do_tasks
def get_polarity(data):
    to_return = []
    for d in data:
        to_return.append(d[1])
    return to_return

def do_read():
    global dataset_fn, dataset_sa
    csv.field_size_limit(sys.maxsize)

    l.log(Severity.INFO, "Started reading dataset for SA")
    with open(os.environ["DATASET_SA"]) as dataset:
        reader = csv.reader(dataset, delimiter=",")
        for [polarity, _, _, _, _, text] in reader:
            dataset_sa.append([text.lower(), polarity])
        dataset_sa = dataset_sa[1:]
    l.log(Severity.INFO, "Finished reading dataset for SA")

    
    l.log(Severity.INFO, "Started reading dataset for FN")
    with open(os.environ["DATASET_FN"]) as dataset:
        reader = csv.reader(dataset, delimiter=",")
        for [_, _, _, text, polarity] in reader:
            dataset_fn.append([text.lower(), polarity])
        dataset_fn = dataset_fn[1:]
    l.log(Severity.INFO, "Finished reading dataset for FN")

def get_score(model, x_train, x_test, y_train, y_test):
    model.fit(x_train, y_train)
    return model.score(x_test, y_test)

def get_train(data):
    (model, x_train, x_test, y_train, y_test) = data
    return get_score(model, x_train, x_test, y_train, y_test)


def do_kfold(model, name, dataset):
    l.log(Severity.INFO, "Started cross validation for: " + name)
    scores = []
    score = 0.0
    kf = KFold(n_splits=10)

    text = get_text(dataset)
    polarity = get_polarity(dataset)

    data = []

    for train_index, test_index in kf.split(text):
        x_train = []
        x_test = []
        y_train = []
        y_test = []
        
        for i in train_index:
            x_train.append(text[i])
            y_train.append(polarity[i])
        for i in test_index:
            x_test.append(text[i])
            y_test.append(polarity[i])

        x_train = vectorizer.fit_transform(x_train)
        x_test = vectorizer.transform(x_test)

        data.append((model, x_train, x_test, y_train, y_test))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for s in executor.map(get_train, data):
            scores.append(s)

    for s in scores:
        score += s
    score /= 10

    l.log(Severity.INFO, "Cross val scores for " + name + "is: " + str(scores))
    l.log(Severity.INFO, "Cross val med score for " + name + "is: " + str(score))
    l.log(Severity.INFO, "Finished cross validation for: " + name)


if __name__ == "__main__":
    do_read()
    #do_kfold(RandomForestClassifier(n_estimators=100, n_jobs=-1), "RandomForest", dataset_fn)
    do_kfold(MultinomialNB(), "Naive Bayes", dataset_sa)
    #do_kfold(svm.SVC(), "SVM - FN", dataset_fn)
    #do_kfold(svm.SVC(), "SVM - SA", dataset_sa)
    wp.abort()