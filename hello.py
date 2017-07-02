#-*- encoding:utf-8 -*-
from flask import Flask,render_template,session,make_response,send_file,request
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,RadioField,TextAreaField,SelectField,FileField
from wtforms.validators import DataRequired,equal_to
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import time
import os
import base64


#初始化
app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] ='synudc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aizai2017@localhost:3306/dc?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(app,use_native_unicode="utf8")
#上传功能相关配置
UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))


#数据库对象
#用户
class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,nullable=False)
    name = db.Column(db.String(64),nullable=True)
    password = db.Column(db.String(64),nullable=False)
    collage = db.Column(db.String(64), nullable=True)
    major = db.Column(db.String(64), nullable=True)
    tel = db.Column(db.String(64),nullable=True)
    usermode = db.Column(db.Integer,db.ForeignKey('user_mode.mid'))
    linkp = db.relationship('User_Project',backref='user')
    def __repr__(self):
        return '<User %r>' % self.username

#学院
class Collage(db.Model):
    __tablename__ = 'collage'
    cid = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(64),unique=True,nullable=False)

#专业
class Major(db.Model):
    __tablename__='major'
    mid=db.Column(db.Integer,primary_key=True)
    mname = db.Column(db.String(64),unique=True)

#用户类型
class User_mode(db.Model):
    __tablename__ = 'user_mode'
    mid = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='mode')
    def __repr__(self):
        return '<User_name %r>' % self.name

#项目
class Project(db.Model):
    __tablename__ = 'project'
    pid = db.Column(db.Integer,primary_key=True)
    pname = db.Column(db.String(64),nullable=False)
    plevel = db.Column(db.String(64))
    collage = db.Column(db.String(64))
    Person_in_charge = db.Column(db.Integer)
    teacher = db.Column(db.String(64))
    describe = db.Column(db.Text)
    status = db.Column(db.Integer)
    doc = db.Column(db.String(64))
    linku = db.relationship('User_Project',backref='project')
    def __repr__(self):
        return  '<Project %r>'%self.pid

#项目状态
class Project_mode(db.Model):
    __tablename__ = 'Project_mode'
    sid = db.Column(db.Integer,primary_key=True)
    status = db.Column(db.String(64),unique=True)

#用户和项目的映射关系
class User_Project(db.Model):
    __tablename__ = 'User_Project'
    id = db.Column(db.Integer,primary_key=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.userid'))
    pid = db.Column(db.Integer,db.ForeignKey('project.pid'))


#表单
#登录页显示的表单
class Login(Form):
    username = StringField("用户名" ,validators=[DataRequired()])
    password = PasswordField("密码" ,validators=[DataRequired()])
    submit = SubmitField('登录')

#注册页显示的表单
class Register(Form):
    username = StringField("学号" ,validators=[DataRequired()])
    name = StringField("姓名" ,validators=[DataRequired()])
    password = PasswordField("密码" ,validators=[DataRequired()])
    repassword = PasswordField("确认密码",validators=[DataRequired(),equal_to('password')])
    #根据数据库里的内容，自动生成学院和专业的下拉表单
    collage = SelectField("学院" ,validators=[DataRequired()],choices=[(x.cname,x.cname) for x in Collage.query.all()])
    major = SelectField("专业", validators=[DataRequired()],choices=[(x.mname,x.mname) for x in Major.query.all()])
    tel = StringField("电话号码")
    submit = SubmitField('注册')

#创建项目页面的表单
class Create_project(Form):
    projectname = StringField("项目名")
    projectlevel= RadioField('项目分级', choices=[('省级', '省级'), ('校级', '校级'),('院级', '院级')])
    collage = StringField("学院")
    teacher = StringField("指导教师")
    describe = TextAreaField("项目简介")
    file = FileField("文档")
    submit = SubmitField('创建')

#加入项目页面的表单
class Join_project(Form):
    projectname = StringField("项目名")
    submit = SubmitField('加入')

#小工具
#根据用户名生成一个由项目构成的列表（项目是数据库一行记录的映射）
def findMyproject(username):
    Userid = User.query.filter_by(username = username).first().userid
    Pid = User_Project.query.filter_by(userid = Userid).all()
    pidlist = [x.pid for x in Pid]
    Prolist = [Project.query.filter_by(pid=x).first() for x in pidlist]
    return Prolist

#生成一个由状态号和状态名组成的元组构成的列表
def createStatuslist():
    a = [(x.sid, x.status) for x in Project_mode.query.all()]
    return a

#根据提供的用户名获取用户现在的权限
def getUserauth(user):
   return User.query.filter_by(username=user).first().usermode

#路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projectManage-manager.html')
def projectManage():
    return render_template('/manager/projectManage-manager.html',pros=Project.query.all(),stalist=createStatuslist())

#完成登录功能
@app.route('/login',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        if username.password==form.password.data:
            session["username"]=username.username
            #判断用户类型
            if username.usermode == User_mode.query.filter_by(name='学生').first().mid:
                return render_template('loginsucc-student.html',name=username.name)
            elif username.usermode == User_mode.query.filter_by(name='管理员').first().mid:
                return render_template('Manager.html', name=username.name)
        else:
            return render_template('loginfail.html')
    return render_template('login.html',form=form)


@app.route('/home-manager.html')
def home_manager():
    return  render_template('home-manager.html')

#我的项目
@app.route('/myproject')
def myproject():
    return render_template('myproject.html',pros=findMyproject(username=session['username']),stalist=createStatuslist())

#完成注册功能
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

#完成创建项目功能
@app.route('/createproject.html',methods=['GET','POST'])
def create_project():
    form=Create_project()
    if form.validate_on_submit():
        pname = Project.query.filter_by(pname=form.projectname.data).first()
        if pname is None:
            #增加各种数据项到数据库
            pro = Project()
            pu=User_Project()
            pro.pname = form.projectname.data
            pro.plevel = form.projectlevel.data
            pro.describe = form.describe.data
            pro.Person_in_charge=session["username"]
            pro.collage = form.collage.data
            pro.teacher = form.teacher.data
            pro.status = Project_mode.query.filter_by(status='未审核').first().sid
            pu.pid=Project.query.filter_by(pname=form.projectname.data).first().pid
            pu.userid=User.query.filter_by(username=Project.query.filter_by(pname=form.projectname.data).first().Person_in_charge).first().userid
            #完成文件上传功能
            file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])+'/start'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            #重命名文件
            fname = secure_filename(form.file.data.filename).split('.',1)[-1]
            unix_time = int(time.time())
            new_filename = str(unix_time) + '.' + fname

            form.file.data.save('upload/start/' + new_filename)
            pro.doc = new_filename
            db.session.add(pu)
            db.session.commit()
            return '创建成功'
        else:
            return '创建失败'
    return render_template('createproject.html', form=form)

#完成用户加入项目功能
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

@app.route('/project/<pid>')
def project(pid):
    pro = Project.query.filter_by(pid=pid).first()
    session['project']=pid
    pchar = User.query.filter_by(username=Project.query.filter_by(pid=pid).first().Person_in_charge).first()
    pmembers = [User.query.filter_by(userid=x.userid).first() for x in User_Project.query.filter_by(pid=pid).all()]
    # 生成用来判断是否显示按钮的变量
    if User_mode.query.filter_by(mid=getUserauth(session['username'])).first().name=='管理员':
        auth=True
    else:
        auth=False
    psta = None
    for x in createStatuslist():#生成用来判断显示什么按钮的变量
        if pro.status == x[0]:
            psta = (x[0],x[1]) #x[0]为状态号，x[1]为状态名
    return render_template('project.html',pro =pro ,pchar=pchar,pmembers=pmembers,auth=auth,pstatus=psta)

#完成项目审核和项目完成路由
@app.route('/auth/<num>')
def auth(num):
    info=None
    pro=Project.query.filter_by(pid=session['project']).first()
    if Project_mode.query.filter_by(sid=num).first().status == '未审核':
        pro.status=Project_mode.query.filter_by(status='未完成').first().sid
        info='审核成功'
    elif Project_mode.query.filter_by(sid=num).first().status == '未完成':
        pro.status=Project_mode.query.filter_by(status='完成').first().sid
        info='项目完成'
    db.session.add(pro)
    db.session.commit()
    return render_template('authsucc.html',info=info)

#下载初始文件路由
@app.route('/start/<filename>', methods=['GET'])
def startdownload(filename):
    response = make_response(send_file(basedir+"/upload/"+'start'+'/'+filename))
    response.headers["Content-Disposition"] = "attachment; filename="+filename+";"
    return response

if __name__ == '__main__':
    manager.run()