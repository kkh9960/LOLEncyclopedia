from flask import Flask, render_template, request, jsonify, url_for

import requests
import jwt

import datetime
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)
from datetime import datetime
from pymongo import MongoClient
# import certifi


# ca = certifi.where();
# client = MongoClient('mongodb+srv://test:sparta@cluster0.q5fchzu.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
# client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('mongodb://13.125.160.207', 27017, username="test", password="test")
db = client.LOLEncyclopedia


@app.route('/')
def main():
    rows = list(db.loldb.find({}, {'_id': False}))
    return render_template("index.html", lists=rows)

@app.route('/write')
def write():
    return render_template("write.html")

@app.route('/show/<int:num>', methods=["GET"])
def show(num):
    rows = db.loldb.find_one({'num': num})
    return render_template('show.html', row=rows)



@app.route("/api/posts", methods=["POST"])
def save_post():
    title_receive = request.form['title_give']
    name_receive = request.form['name_give']
    position_receive = request.form['position_give']
    star_receive = request.form['star_give']
    desc_receive = request.form['desc_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'img{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)



    lists = list(db.loldb.find({}, {'_id': False}))
    count = len(lists) + 1


    doc = {
        'num': count,
        'image': f'{filename}.{extension}',
        'title': title_receive,
        'name': name_receive,
        'position': position_receive,
        'star': star_receive,
        'desc': desc_receive,
        'num': count
    }

    db.loldb.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


@app.route('/plus')
def plus():
    return render_template('detail.html')


@app.route('/api/posts')
def home():
    return render_template('write.html')


@app.route("/lolplus", methods=["POST"])
def chat_post():
    chat_receive = request.form['comment_give']

    doc = {
        'chat': chat_receive
    }

    db.lolplus.insert_one(doc)

    return jsonify({'msg': 'post(기록) 연결'})


@app.route("/lolplus", methods=["GET"])
def chat_get():
    lolplus_list = list(db.lolplus.find({}, {'_id': False}))

    return jsonify({'chat_db': lolplus_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
