from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient

import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.qvjmyb9.mongodb.net/?retryWrites=true&w=majority' , tlsCAFile=ca)
db = client.week1_team
app = Flask(__name__)


@app.route('/')
def plus():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/lolplus", methods=["POST"])
def chat_post():
    chat_receive = request.form['comment_give']

    doc = {
        'chat':chat_receive
    }

    db.lolplus.insert_one(doc)

    return jsonify({'msg': 'post(기록) 연결'})


@app.route("/lolplus", methods=["GET"])
def chat_get():
    lolplus_list = list(db.lolplus.find({}, {'_id': False}))

    return jsonify({'chat_db': lolplus_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
