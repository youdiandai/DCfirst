from flask import Flask,render_template,session,redirect,url_for
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,RadioField
from wtforms.validators import Required,NumberRange
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] ='synudc'
dbaddress = 'mysql://root:aizai2017@127.0.0.1/dc'
app.config['SQLALCHEMY_DATABASE_URL']=dbaddress
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    password = db.Column(db.Integer,nullable=False)
    collage = db.Column(db.String(64), nullable=False)
    tel = db.Column(db.Integer,nullable=False)
    usermode = db.Column(db.String(64),nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

class User_mode(db.Model):
    __tablename__ = 'user_name'
    mid = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    def __repr__(self):
        return '<User_name %r>' % self.name

class Project(db.Model):
    __tablename__ = 'project'
    pid = db.Column(db.Integer,primary_key=True)
    pname = db.Column(db.Text,nullable=False)
    Person_in_charge = db.Column(db.Integer,nullable=False)
    docurl = db.Column(db.Text)
    def __repr__(self):
        return  '<Project %r>'%self.pid

class User_Project(db.Model):
    __tablename__ = 'User_Project'
    userid = db.Column(db.Integer,primary_key=True)
    pid = db.Column(db.Integer,primary_key=True)
    def __repr__(self):
        return '<User_Project %r %r>'%self.userid,self.pid


class Login(Form):
    username = StringField("用户名",validators=[Required()])
    password = PasswordField("密码",validators=[Required()])
    mode = RadioField('用户类型', choices=[('admin', '管理员'), ('user', '用户')])
    submit = SubmitField('登录')

class Register(Form):
    username = StringField("学号",validators=[Required()])
    name = StringField("姓名",validators=[Required()])
    password = PasswordField("密码",validators=[Required()])
    repassword = PasswordField("再次输入密码",validators=[Required()])
    collage = StringField("学院",validators=[Required()])
    tel = StringField("电话号码")
    submit = SubmitField('注册')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        session['password'] = form.password.data
        session['username'] = form.username.data
        session['mode'] = form.mode.data
        return redirect(url_for('login'))
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    register = Register()
    if register.validate_on_submit():
        session['username']=register.username.data
        session['name']=register.name.data
        session['password']=register.password.data
        session['repassword']=register.repassword.data
        session['collage']=register.collage.data
        session['tel']=register.tel.data
        return  redirect(url_for('register'))
    return render_template('register.html',form=register)

if __name__ == '__main__':
    manager.run()