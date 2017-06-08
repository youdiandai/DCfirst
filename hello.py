from flask import Flask,render_template,session,redirect,url_for
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,RadioField,TextAreaField
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
    plevel = db.Column(db.String(64),unique=True)
    collage = db.Column(db.String(64), unique=True)
    Person_in_charge = db.Column(db.Integer)
    describe = db.Column(db.Text)
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

class Create_project(Form):
    projectname = StringField("项目名", validators=[Required()])
    projectlevel= mode = RadioField('项目分级', choices=[('省级', '省级'), ('校级', '校级'),('院级', '院级')])
    collage = StringField("学院", validators=[Required()])
    describe = TextAreaField("项目简介", validators=[Required()])
    submit = SubmitField('提交')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        if username.password==form.password.data:
            session["username"]=username.username
            return render_template("loginsucc.html",name=username.name)
        else:
            return render_template('loginfail.html')
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
            return render_template("registersucc.html")
        else:
            return render_template('registerfail.html')
    return render_template('register.html',form=register)

@app.route('/create_project',methods=['GET','POST'])
def create_project():
    form=Create_project()
    if form.validate_on_submit():
        pname = Project.query.filter_by(pname=form.projectname.data).first()
        if pname is None:
            pro = Project()
            pro.pname = form.projectname.data
            pro.plevel = form.projectlevel.data
            pro.describe = form.describe.data
            pro.collage = form.collage.data
            db.session.add(pro)
            db.session.commit()
            return render_template("registersucc.html")
        else:
            return render_template('registerfail.html')
    return render_template('create_project.html', form=form)



if __name__ == '__main__':
    manager.run()