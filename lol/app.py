from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename

from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'LOL'

client = MongoClient('52.78.245.130', 27017, username="test", password="test")
db = client.lol


@app.route('/index')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    words = list(db.lol.find({}, {"_id": False}))
    return render_template("index.html", words=words)
    # 토큰 검색
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/lol', methods=['GET'])
def show_diary():
    lols = list(db.lol.find({}, {'_id': False}))
    return jsonify({'all_lol': lols})


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        # "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        # "profile_pic": "",                                          # 프로필 사진 파일 이름
        # "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        # "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    # 찾아서 하나라도 있으면 T 없으면 F
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 토큰을 받아
        user_info = db.users.find_one({"username": payload["id"]})
        # 유저 db에 아이디를 꺼낸다
        post_id_receive = request.form["post_id_give"]
        type_receive = request.form["type_give"]
        action_receive = request.form["action_give"]
        doc = {
            "post_id": post_id_receive,
            "username": user_info["username"],
            "type": driver.current_url
        }
        if action_receive == "like":
            db.likes.insert_one(doc)
        else:
            db.likes.delete_one(doc)
        count = db.likes.count_documents({"post_id": post_id_receive, "type": type_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
        # 좋아요 수 변경
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


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

    lists = list(db.lol.find({}, {'_id': False}))
    count = len(lists) + 1

    doc = {
        'num': count,
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


@app.route('/show/<int:num>', methods=["GET"])
def show(num):
    rows = db.lol.find_one({'num': num})
    words = list(db.lol.find({}, {"_id": False}))
    return render_template('show.html', row=rows, words=words)


@app.route("/lolplus", methods=["POST"])
def chat_post():
    chat_receive = request.form['comment_give']
    name_receive = request.form['name_give']

    doc = {
        'chat': chat_receive,
        'name': name_receive,
    }

    db.lolplus.insert_one(doc)

    return jsonify({'msg': '댓글등록완료'})


@app.route("/show/<int:num>", methods=["GET"])
def chat_get(num):
    chatsnus = db.lolplus.find_one({'ch_num': num})

    return render_template('/show/<int:num>', chatnu=chatsnus)


# @app.route('/api/save_word', methods=['POST'])
# def save_word():
#     # 단어 저장하기
#     return jsonify({'result': 'success', 'msg': '단어 저장'})
#
#
# @app.route('/api/delete_word', methods=['POST'])
# def delete_word():
#     # 단어 삭제하기
#     return jsonify({'result': 'success', 'msg': '단어 삭제'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
