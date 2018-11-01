#import all
from flask import Flask, render_template

app = Flask(__name__)

#page route

@app.route('/')#첫 페이지
def index():
    return render_template('index.html')

@app.route('/table')#도서 전체 목록 페이지
def table():
    return render_template('table.html')

@app.route('/mypage')#마이페이지
def mypage():
    return render_template('mypage.html')

#앱 실행
if __name__=='__main__':
    app.run(debug=True)