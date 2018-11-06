#import all
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

#데이터베이스 관리
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/sola/Desktop/bookrental/booklist.db'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

#도서 데이터베이스
class Booklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    kategorie = db.Column(db.String(50))
    status = db.Column(db.String(50))
    date = db.Column(db.String(50))

#사용자 데이터베이스
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True)

#사용자 call back
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET','POST'])#로그인
def login():
    form = LoginForm
    return render_template('login.html')

@app.route('/logout')#로그아웃
def logout():
    logout_user()
    return redirect(url_for('index'))

#page route
@app.route('/')#첫 페이지
def index():
    user = User.query.filter_by(username='sola').first()
    login_user(user)
    return render_template('index.html')

@app.route('/mypage')#마이페이지
@login_required ##로그인한 사용자만 들어갈 수 있게 설정
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

@app.route('/search', methods=['POST'])#검색 도서 목록
def search():
    book = request.form['book']
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