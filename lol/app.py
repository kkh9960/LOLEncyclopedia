from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def main():
    myname = "Sparta"
    return render_template("index.html", name = myname)


@app.route('/detail')
def detail():
    r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
    #requests에서 겟 요청을 보냄
    response = r.json()
    #제이슨형태로 만들어줘
    rows = response['RealtimeCityAir']['row']
    #rows에 저걸 보내줘
    word_recevie = request.args.get("word_give")
    print(word_recevie)
    return render_template("detail.html", rows=rows)
    #앞에 rows는 변수선언 뒤에 rows는 위에 리스폰 리얼타임시티 로우를 보냄


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)