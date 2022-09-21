from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests

from datetime import datetime

app = Flask(__name__)

client = MongoClient('43.200.181.231', 27017, username="test", password="test")
db = client.lol


@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    words = list(db.lol.find({}, {"_id": False}))
    return render_template("index.html", words=words)


@app.route('/lol', methods=['GET'])
def show_diary():
    lols = list(db.lol.find({}, {'_id': False}))
    return jsonify({'all_lol': lols})


@app.route('/lol', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    name_receive = request.form['name_give']
    position_receive = request.form['position_give']
    desc_receive = request.form['desc_give']
    star_receive = request.form['star_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title': title_receive,
        'name': name_receive,
        'position': position_receive,
        'desc': desc_receive,
        'star': star_receive,
        'file': f'{filename}.{extension}'
    }

    db.lol.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route('/detail')
def detail():
    # API에서 단어 뜻 찾아서 결과 보내기
    return render_template("detail.html")


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    return jsonify({'result': 'success', 'msg': '단어 저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    return jsonify({'result': 'success', 'msg': '단어 삭제'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
