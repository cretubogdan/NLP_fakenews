import sys
sys.path.insert(0, '../modules')
import os
import csv
from Logger import *

from thundersvm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score

l = Logger()

dataset_sa = []

vectorizer = TfidfVectorizer(min_df=5, max_df=0.8, use_idf=True)

def get_text(data):
    to_return = []
    for (text, _) in data:
        to_return.append(text)
    return to_return

def get_polarity(data):
    to_return = []
    for (_, polarity) in data:
        to_return.append(polarity)
    return to_return

def get_number(number):
    if '4' in number:
        return 4
    elif '2' in number:
        return 2
    elif '0' in number:
        return 0

    return number

def do_read():
    global dataset_sa
    csv.field_size_limit(sys.maxsize)

    l.log(Severity.INFO, "Started reading dataset for SA")
    with open(os.environ["DATASET_SA"]) as dataset:
        reader = csv.reader(dataset, delimiter=",")
        for [polarity, _, _, _, _, text] in reader:
            dataset_sa.append([text.lower(), get_number(polarity)])
        dataset_sa = dataset_sa[1:]
    l.log(Severity.INFO, "Finished reading dataset for SA")

def do_kfold(model):
    global dataset_sa, vectorizer
    l.log(Severity.INFO, "Started kfold")

    text = get_text(dataset_sa)
    polarity = get_polarity(dataset_sa)

    X = vectorizer.fit_transform(text)

    m_score = 0.0
    res = cross_val_score(model, X, polarity, scoring='recall_macro', cv=10)
    l.log(Severity.INFO, str(res))
    for score in res:
        m_score += score
        l.log(Severity.INFO, "Score: " + str(score))

    m_score /= 10.0
    l.log(Severity.INFO, "Medium score: " + str(m_score))

    l.log(Severity.INFO, "Finished kfold")


if __name__ == "__main__":
    do_read()
    do_kfold(SVC(kernel='rbf', gamma='auto', n_jobs = -1))