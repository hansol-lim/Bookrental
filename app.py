#import all
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/sola/Desktop/bookrental/booklist.db'

db = SQLAlchemy(app)

#데이터 베이스 칼럼
class Booklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    kategorie = db.Column(db.String(50))
    status = db.Column(db.String(50))
    date = db.Column(db.String(50))

#page route
@app.route('/')#첫 페이지
def index():

    return render_template('index.html')

@app.route('/mypage')#마이페이지
def mypage():
    return render_template('mypage.html')

@app.route('/add')#도서등록페이지
def add():
    return render_template('add.html')

@app.route('/addbook', methods=['POST'])#등록한 도서를 데이터 베이스에 추가
def addbook():
    name = request.form['name']
    author = request.form['author']
    kategorie = request.form['kategorie']
    status = request.form['status']
    date = request.form['date']

    booklist = Booklist(name=name,author=author,kategorie=kategorie,status=status,date=date)

    db.session.add(booklist)
    db.session.commit()

    return redirect(url_for('add'))

@app.route('/search', methods=['POST'])#검색기능
def search():
    book = request.form['book']
    
    #lists = Booklist.query.filter_by(name=book).all()
    #lists = Booklist.query.filter_by(kind.like('%book%')).all()
    lists = Booklist.query.filter(Booklist.name.like('%%%s%%' % book)).all()
    return render_template('table.html', lists=lists)

@app.route('/table')#도서 목록 페이지
def table():
    lists = Booklist.query.all()
    return render_template('table.html', lists=lists)

@app.route('/table2')#대출 가능 목록 페이지
def table2():

    lists = Booklist.query.filter_by(status='대출가능').all()

    return render_template('table.html', lists=lists)

#앱 실행
if __name__=='__main__':
    app.run(debug=True)