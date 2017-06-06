from flask import Flask,render_template,session,redirect,url_for
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,RadioField
from wtforms.validators import Required,NumberRange
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] ='synudc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aizai2017@localhost:3306/dc?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(app,use_native_unicode="utf8")

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,nullable=False)
    name = db.Column(db.String(64),nullable=False)
    password = db.Column(db.String(64),nullable=False)
    collage = db.Column(db.String(64), nullable=False)
    tel = db.Column(db.String(64),nullable=False)
    usermode = db.Column(db.Integer,db.ForeignKey('user_mode.mid'))
    linkp = db.relationship('User_Project',backref='user')
    def __repr__(self):
        return '<User %r>' % self.username

class User_mode(db.Model):
    __tablename__ = 'user_mode'
    mid = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='mode')
    def __repr__(self):
        return '<User_name %r>' % self.name

class Project(db.Model):
    __tablename__ = 'project'
    pid = db.Column(db.Integer,primary_key=True)
    pname = db.Column(db.Text,nullable=False)
    Person_in_charge = db.Column(db.Integer,nullable=False)
    docurl = db.Column(db.Text)
    linku = db.relationship('User_Project',backref='project')
    def __repr__(self):
        return  '<Project %r>'%self.pid

class User_Project(db.Model):
    __tablename__ = 'User_Project'
    id = db.Column(db.Integer,primary_key=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.userid'))
    pid = db.Column(db.Integer,db.ForeignKey('project.pid'))
    def __repr__(self):
        return '<User_Project %r %r>'%self.userid,self.pid


class Login(Form):
    username = StringField("用户名" ,validators=[Required()])
    password = PasswordField("密码" ,validators=[Required()])
    mode = RadioField('用户类型', choices=[('admin', '管理员'), ('user', '用户')])
    submit = SubmitField('登录')

class Register(Form):
    username = StringField("学号" ,validators=[Required()])
    name = StringField("姓名" ,validators=[Required()])
    password = PasswordField("密码" ,validators=[Required()])
    repassword = PasswordField("再次输入密码",validators=[Required()])
    collage = StringField("学院" ,validators=[Required()])
    tel = StringField("电话号码")
    submit = SubmitField('注册')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        if username.password==form.password.data:
            return '<h1>登陆成功</h1>'
        else:
            return '<h1>账号或密码错误</h1>'
        return redirect(url_for('login'))
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    register = Register()
    if register.validate_on_submit():
        username =User.query.filter_by(username=register.username.data).first()
        if username is None:
            user=User()
            user.username=register.username.data
            user.name=register.name.data
            user.password=register.password.data
            user.collage=register.collage.data
            user.tel = register.tel.data
            db.session.add(user)
            db.session.commit()
            return  '<h1>注册成功</h1>'
    return render_template('register.html',form=register)

if __name__ == '__main__':
    manager.run()