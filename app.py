#import all
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy #데이터베이스
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap # 이건 일단 보류
from wtforms import StringField, PasswordField, BooleanField #로그인 폼
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm 
from werkzeug.security import generate_password_hash, check_password_hash #비밀번호 보안문제

app = Flask(__name__)

#데이터베이스 관리
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/sola/Desktop/bookrental/booklist.db'
app.config['SECRET_KEY'] = 'thisissecret' #로그인을 넣으려면 꼭 필요하다.

bootstrap = Bootstrap(app) #..보류

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#도서 데이터베이스 칼럼 ... 나중에 이미지 파일 추가
class Booklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    kategorie = db.Column(db.String(50))
    status = db.Column(db.String(50))
    date = db.Column(db.String(50))

#사용자 데이터베이스 칼럼 ... 슬랙과 연동하는 문제 추후 해결
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

#로그인 기능
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm): #로그인 화면 구성
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm): #가입 화면 구성
    email = StringField('email', validators=[InputRequired(), Email(message='Invaild email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/', methods=['GET','POST'])#로그인 페이지
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))
        return '이름이나 비밀번호를 다시 확인해 주세요'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])#가입페이지
def signup():
    
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/logout')#로그아웃
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#page route
@app.route('/home')#로그인 후 첫 페이지
@login_required #로그인한 사용자만 접근 가능능
def index():
    return render_template('index.html' , name=current_user.username)

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
    return render_template('table.html', lists=lists, name=current_user.username)

@app.route('/table')#도서 목록 페이지
def table():
    lists = Booklist.query.all()
    return render_template('table.html', lists=lists, name=current_user.username)

@app.route('/table2')#대출 가능 목록 페이지
def table2():
    lists = Booklist.query.filter_by(status='대출가능').all()
    return render_template('table.html', lists=lists, name=current_user.username)

#앱 실행
if __name__=='__main__':
    app.run(debug=True)