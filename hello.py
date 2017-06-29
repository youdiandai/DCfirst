from flask import Flask,render_template,session,redirect,url_for
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,RadioField,TextAreaField,SelectField
from wtforms.validators import DataRequired,equal_to
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
    major = db.Column(db.String(64), nullable=False)
    tel = db.Column(db.String(64),nullable=False)
    usermode = db.Column(db.Integer,db.ForeignKey('user_mode.mid'))
    linkp = db.relationship('User_Project',backref='user')
    def __repr__(self):
        return '<User %r>' % self.username

class Collage(db.Model):
    __tablename__ = 'collage'
    cid = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(64),unique=True,nullable=False)

class Major(db.Model):
    __tablename__='major'
    mid=db.Column(db.Integer,primary_key=True)
    mname = db.Column(db.String(64),unique=True)

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
    pname = db.Column(db.String(64),nullable=False)
    plevel = db.Column(db.String(64))
    collage = db.Column(db.String(64))
    Person_in_charge = db.Column(db.Integer)
    describe = db.Column(db.String(64))
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
    username = StringField("用户名" ,validators=[DataRequired()])
    password = PasswordField("密码" ,validators=[DataRequired()])
    submit = SubmitField('登录')

class Register(Form):
    username = StringField("学号" ,validators=[DataRequired()])
    name = StringField("姓名" ,validators=[DataRequired()])
    password = PasswordField("密码" ,validators=[DataRequired()])
    repassword = PasswordField("确认密码",validators=[DataRequired(),equal_to('password')])
    collage = SelectField("学院" ,validators=[DataRequired()],choices=[(x.cname,x.cname) for x in Collage.query.all()])
    major = SelectField("专业", validators=[DataRequired()],choices=[(x.mname,x.mname) for x in Major.query.all()])
    tel = StringField("电话号码")
    submit = SubmitField('注册')

class Create_project(Form):
    projectname = StringField("项目名")
    projectlevel= RadioField('项目分级', choices=[('省级', '省级'), ('校级', '校级'),('院级', '院级')])
    collage = StringField("学院")
    describe = TextAreaField("项目简介")
    submit = SubmitField('创建')

class Join_project(Form):
    projectname = StringField("项目名")
    submit = SubmitField('加入')

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
            if username.usermode == User_mode.query.filter_by(name='学生').first().mid:
                return render_template('/student/loginsucc-student.html',name=username.name)
            elif username.usermode == User_mode.query.filter_by(name='管理员').first().mid:
                return render_template('/manager/Manager.html', name=username.name)
        else:
            return render_template('loginfail.html')
    return render_template('login.html',form=form)

@app.route('/myproject')
def myproject():
    return render_template('myproject.html')

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
            user.major=register.major.data
            user.tel = register.tel.data
            user.usermode = User_mode.query.filter_by(name='学生').first().mid

            db.session.add(user)
            db.session.commit()
            return render_template("registersucc.html")
        else:
            return render_template('registerfail.html')
    return render_template('register.html',form=register)

@app.route('/createproject',methods=['GET','POST'])
def create_project():
    form=Create_project()
    if form.validate_on_submit():
        pname = Project.query.filter_by(pname=form.projectname.data).first()
        if pname is None:
            pro = Project()
            pu=User_Project()
            pro.pname = form.projectname.data
            pro.plevel = form.projectlevel.data
            pro.describe = form.describe.data
            pro.Person_in_charge=session["username"]
            pro.collage = form.collage.data
            db.session.add(pro)
            db.session.commit()
            pu.pid=Project.query.filter_by(pname=form.projectname.data).first().pid
            pu.userid=User.query.filter_by(username=Project.query.filter_by(pname=form.projectname.data).first().Person_in_charge).first().userid
            db.session.add(pu)
            db.session.commit()
            return '创建成功'
        else:
            return '创建失败'
    return render_template('createproject.html', form=form)


@app.route('/join_project',methods=['GET','POST'])
def join_project():
    form = Join_project()
    if form.validate_on_submit():
        pud = User_Project.query.filter_by(pid=Project.query.filter_by(pname=form.projectname.data).first().pid,userid=User.query.filter_by(username=session["username"]).first().userid).first()
        if pud is None:
            pu=User_Project()
            pu.userid=User.query.filter_by(username=session["username"]).first().userid
            pu.pid=Project.query.filter_by(pname=form.projectname.data).first().pid
            db.session.add(pu)
            db.session.commit()
            return '加入成功'
        else:
            return '加入失败'
    return render_template('join_project.html',form=form)

if __name__ == '__main__':
    manager.run()