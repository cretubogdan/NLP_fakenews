import sys
sys.path.insert(0, '../modules')
from Logger import *
from DBManager import *
from flask import Flask, render_template, request, jsonify
import random

PORT_NO = 80
HOST = "0.0.0.0"

app = Flask(__name__)
l = Logger()
db = DBManager()
collection_users = "users"
collection_news = "news"

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

@app.route("/make_testnews", methods=["POST"])
def make_testnews():
    req_data = request.get_json()
    #TODO 3
    print("\n\n\n\n" + str(req_data) + "\n\n\n\n")
    return "OK"

@app.route("/make_train_logs")
def make_train_logs():
    return "MERGE"

@app.route("/make_train", methods=["POST"])
def make_train():
    req_data = request.get_json()
    #TODO 4
    print("\n\n\n\n" + str(req_data) + "\n\n\n\n")
    return "OK"

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
    news_db = db.find(query, collection_news)
    while count_req_news > 0:
        index = random.randint(0, news_db.count() - 1)
        news.append(make_findnews_helper(news_db, index))
        count_req_news -= 1

    return jsonify(results=news)


if __name__ == "__main__":
    l.log(Severity.INFO, "Sever started {0}:{1}".format(HOST, PORT_NO))
    app.run(debug=True, host=HOST, port=PORT_NO)