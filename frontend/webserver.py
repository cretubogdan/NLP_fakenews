import sys
sys.path.insert(0, '../modules')
import os
import subprocess
from DBManager import *
from flask import Flask, render_template, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import random

PORT_NO = 80
HOST = "0.0.0.0"

app = Flask(__name__)
db = DBManager()
collection_users = "users"
collection_admins = "admins"
collection_news = "news"
path_logs_retrain = ""
stop_logs = False

collection_dump_models_fn_rf = "models_dump_randomforest"
collection_dump_features_fn_rf = "features_dump_randomforest"
collection_dump_models_sa_nb = "models_dump_naivebayse"
collection_dump_features_sa_nb = "features_dump_tfidf_naivebayse"
collection_dump_models_fn_svm = "models_dump_svm_fn"
collection_dump_features_fn_svm = "features_dump_svm_fn"
collection_dump_models_sa_svm = "models_dump_svm_sa"
collection_dump_features_sa_svm = "features_dump_svm_sa"

model_fn_rf = pickle.loads(db.grid_find(collection_dump_models_fn_rf))
vectorizer_fn_rf = pickle.loads(db.grid_find(collection_dump_features_fn_rf))
model_sa_nb = pickle.loads(db.grid_find(collection_dump_models_sa_nb))
vectorizer_sa_nb = pickle.loads(db.grid_find(collection_dump_features_sa_nb))
model_fn_svm = pickle.loads(db.grid_find(collection_dump_models_fn_svm))
vectorizer_fn_svm = pickle.loads(db.grid_find(collection_dump_features_fn_svm))
model_sa_svm = pickle.loads(db.grid_find(collection_dump_models_sa_svm))
vectorizer_sa_svm = pickle.loads(db.grid_find(collection_dump_features_sa_svm))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/testnews")
def testnews():
    return render_template('testnews.html')

@app.route("/train")
def train():
    return render_template('train.html')

@app.route("/findnews")
def findnews():
    return render_template('findnews.html')

@app.route("/make_signin", methods=["POST"])
def make_signin():
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']
    users = db.find(None, collection_users)
    for user in users:
        if user['username'] == username and user['password'] == password:
            return "OK"

    return "Wrong username or password!"

@app.route("/make_signup", methods=["POST"])
def make_signup():
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']
    email = req_data['email']
    users = db.find(None, collection_users)
    for user in users:
        if user['username'] == username:
            return "Username is already registred!"
        elif user['email'] == email:
            return "An user is already registred with this email!"
    
    db.insert(req_data, collection_users)

    return "OK"

def do_predict(model_fn_text, model_sa_text, text):
    global model_fn_rf, model_fn_svm, model_sa_nb, model_sa_svm, vectorizer_fn_rf, vectorizer_fn_svm, vectorizer_sa_nb, vectorizer_sa_svm
    model_fn = None
    model_sa = None
    vectorizer_fn = None
    vectorizer_sa = None

    res_fn = None
    res_sa = "not tested"
    news = [text.lower()]

    if model_fn_text == "SVM - Fake News":
        model_fn = model_fn_svm
        vectorizer_fn = vectorizer_fn_svm
    elif model_fn_text == "Random Forest - Fake News":
        model_fn = model_fn_rf
        vectorizer_fn = vectorizer_fn_rf
    if model_sa_text == "SVM - Sentiment Analisys":
        model_sa = model_sa_svm
        vectorizer_sa = vectorizer_sa_svm
    elif model_sa_text == "Naive Bayes - Sentiment Analisys":
        model_sa = model_sa_nb
        vectorizer_sa = vectorizer_sa_nb

    tf_idf = vectorizer_fn.transform(news)
    result = int(model_fn.predict(tf_idf)[0])
    if result == 0:
        res_fn = "not fake"
    else:
        res_fn = "fake"

    if res_fn == "fake":
        tf_idf = vectorizer_sa.transform(news)
        result = int(model_sa.predict(tf_idf)[0])
        if result == 0:
            res_sa = "negative"
        elif result == 4:
            res_sa = "positive"
        else:
            res_sa = "neutral"

    return (res_fn, res_sa)

@app.route("/make_testnews", methods=["POST"])
def make_testnews():
    to_return = ""
    req_data = request.get_json()

    model_fn_text = req_data["model_fn"]
    model_sa_text = req_data["model_sa"]
    text = req_data["text"]
    
    (res_fn, res_sa) = do_predict(model_fn_text, model_sa_text, text)
    
    to_return += "RESULT FAKE NEWS:\n"
    to_return += "\tMODEL: {0}\n".format(model_fn_text)
    to_return += "\tPREDICTION CLASS: {0}\n".format(res_fn)
    if res_fn == "fake":
        to_return += "RESULT SENTIMENT ANALYSIS:\n"
        to_return += "\tMODEL: {0}\n".format(model_sa_text)
        to_return += "\tPREDICTION CLASS: {0}\n".format(res_sa)

    return to_return

@app.route("/make_train_logs", methods=["POST"])
def make_train_logs():
    global path_logs_retrain, stop_logs
    if stop_logs == False:
        to_return = ""
        lines = []

        try:
            with open(path_logs_retrain, "r") as file:
                reader = file.readlines()
                for line in reader:
                    lines.append(line)
                try:
                    lines = lines[1:]
                except:
                    pass
        except:
            pass
        
        for line in lines:
            to_return += line

        if "WorkPool made a new abort" in to_return:
            stop_logs = True

        return to_return
    else:
        stop_logs = False
        return "FINISHED"

def make_train_helper(username):
    admins = db.find(None, collection_admins)
    for admin in admins:
        if admin['username'] == username:
            return True
    return False

@app.route("/make_train", methods=["POST"])
def make_train():
    global path_logs_retrain
    req_data = request.get_json()
    if (make_train_helper(req_data["username"])):
        path = "../"
        path_logs_retrain = ""
        model = req_data["model"]
        if model == "Naive Bayes - Sentiment Analisys":
            path += "naive_bayse/start_naivebayse.sh"
            path_logs_retrain = "/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/naive_bayse/logs"
        elif model == "Random Forest - Fake News":
            path += "random_forest/start_randomforest.sh"
            path_logs_retrain = "/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/random_forest/logs"
        elif model == "SVM - Fake News":
            path += "SVM_FN/start_svm_fn.sh"
            path_logs_retrain = "/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/SVM_FN/logs"
        elif model == "SVM - Sentiment Analisys":
            path += "SVM_SA/start_svm_sa.sh"
            path_logs_retrain = "/Users/mihnea-bogdancretu/Desktop/licenta/NLP_fakenews/SVM_SA/logs"
        else:
            return "You have to choose an algorithm for retrain!"

        n = os.fork()

        if n == 0:
            os.system(path)
            

        return "OK"
    else:
        return "You need administrator privileges to use this feature!"

def make_findnews_helper(news_db, index):
    count = 0
    for i in news_db:
        if count == index:
            return i
        count += 1
    return None

@app.route("/make_findnews", methods=["POST"])
def make_findnews():
    req_data = request.get_json()
    news = []
    count_req_news = int(req_data['count_news'])
    query = {"_id" : False}
    news_db = db.find_2(query, collection_news)
    while count_req_news > 0:
        index = random.randint(0, news_db.count() - 1)
        news.append(make_findnews_helper(news_db, index))
        count_req_news -= 1

    return jsonify(results=news)


if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT_NO)