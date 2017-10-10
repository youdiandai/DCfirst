#-*- encoding:utf-8 -*-
from flask import Flask,render_template,session,make_response,send_file,request
from flask_script import Manager
from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField,RadioField,TextAreaField,SelectField,FileField
from flask_migrate import Migrate,MigrateCommand
from wtforms.validators import DataRequired,equal_to,Email
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail,Message
from werkzeug.utils import secure_filename
from threading import Thread
import time
import os
import datetime



#初始化
app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] ='synudc'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT']=25
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[DC]'
app.config['FLASKY_MAIL_SENDER']='DCfirst Admin<18504285660@163.com>'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','zip','rar'])
db = SQLAlchemy(app,use_native_unicode="utf8")
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
mail = Mail(app)
login_manager = LoginManager()
login_manager.login_view='/login'
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"
#上传功能相关配置
UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))

#邮件
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr



#数据库对象
# 创建参赛队伍
joincom = db.Table('joincom', db.Column('User_id', db.Integer, db.ForeignKey('user.userid')),db.Column('Competition_id', db.Integer, db.ForeignKey('Competition.Cid')))

#用户
class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(220),unique=True,nullable=False)
    name = db.Column(db.String(220),nullable=True)
    password = db.Column(db.String(220),nullable=False)
    collage = db.Column(db.String(220), nullable=True)
    major = db.Column(db.String(220), nullable=True)
    tel = db.Column(db.String(220),nullable=True)
    email = db.Column(db.String(220),nullable=True)
    usermode = db.Column(db.Integer,db.ForeignKey('user_mode.mid'))
    linkp = db.relationship('User_Project',backref='user')
    Competitions = db.relationship('Competition',secondary=joincom,backref=db.backref('users',lazy='dynamic'),lazy='dynamic')
    def __repr__(self):
        return '<User %r>' % self.username
    def getUserid(self,username):
        return self.query.filter_by(username=username).first().userid


# 用户类型
class User_mode(db.Model):
    __tablename__ = 'user_mode'
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220), unique=True)
    users = db.relationship('User', backref='mode')

    def __repr__(self):
        return '<User_name %r>' % self.name


# 用户和项目的映射关系
class User_Project(db.Model):
    __tablename__ = 'User_Project'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    pid = db.Column(db.Integer, db.ForeignKey('project.pid'))


#学院
class Collage(db.Model):
    __tablename__ = 'collage'
    cid = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(220),unique=True,nullable=False)

#专业
class Major(db.Model):
    __tablename__='major'
    mid=db.Column(db.Integer,primary_key=True)
    mname = db.Column(db.String(220),unique=True)


#项目
class Project(db.Model):
    __tablename__ = 'project'
    pid = db.Column(db.Integer,primary_key=True)#项目系统
    secondTeacher = db.Column(db.String(220),nullable=True)#第二指导教师
    proID = db.Column(db.String(220),nullable=True) #项目编号
    Pname = db.Column(db.String(220),nullable=False)#项目名称
    Plevel = db.Column(db.String(220),nullable=True)#项目级别
    Pclass = db.Column(db.String(220),nullable=True)#项目类别
    Collage = db.Column(db.String(220),nullable=True)#学院
    Deferred_problems = db.Column(db.String(220),nullable=True)#延期结题
    Appraising = db.Column(db.String(220),nullable=True)#评优
    Person_in_charge = db.Column(db.Integer,nullable=True)#负责人
    Teacher = db.Column(db.String(220),nullable=True)#指导教师
    ForTeacher_ID = db.Column(db.Integer,db.ForeignKey('ForTeacher.id'))#校外导师
    Describe = db.Column(db.Text,nullable=True)#项目简介
    Status = db.Column(db.Integer,nullable=True)#项目状态
    StartDate = db.Column(db.String(220),nullable=True)#立项日期
    PlanDate = db.Column(db.String(220),nullable=True)#项目周期
    MidSubdate = db.Column(db.String(220),nullable=True)#中期报告提交日期
    EndSubdate = db.Column(db.String(220),nullable=True)#结题提交日期
    EndDate = db.Column(db.String(220),nullable=True)#项目结束日期
    ReassonsForApplication = db.Column(db.Text,nullable=True)#申请理由
    ProjectPlan = db.Column(db.Text,nullable=True)#项目方案
    Innovate = db.Column(db.Text,nullable=True)#特色和创新点
    Schedule = db.Column(db.Text,nullable=True)#项目进度安排
    Budget = db.Column(db.Integer,nullable=True)#项目经费预算
    BudgetPlan = db.Column(db.Text,nullable=True)#经费使用计划
    ExpectedResults = db.Column(db.Text,nullable=True)#项目预期成果
    TeaStarOpinion = db.Column(db.Text,nullable=True)#指导教师意见（立项）
    CollStarOpinion = db.Column(db.Text,nullable=True)#学院意见
    SchStarOpinion = db.Column(db.Text,nullable=True)#学校意见（立项）
    MidProgress= db.Column(db.Text,nullable=True)#工作进展
    MidResults = db.Column(db.Text,nullable=True)#中期成果
    ResultsDescribe = db.Column(db.Text,nullable=True)#项目成果简介
    ResultsType = db.Column(db.Integer,nullable=True)#项目成果形式
    ResultsSummary = db.Column(db.Text,nullable=True)#项目总结报告
    ResultsNum = db.Column(db.Integer,nullable=True)#成果编号
    Problems = db.Column(db.Text,nullable=True)#存在的问题和建议
    TeaMidOpinion = db.Column(db.Text,nullable=True)#指导教师意见（中期）
    DCCenterMidOpinion = db.Column(db.Text,nullable=True)#大创中心意见（中期）
    SchMidOpinion = db.Column(db.Text,nullable=True)#学院意见（中期）
    TeaEndOpinion = db.Column(db.Text,nullable=True)#项目指导教师意见（结题）
    CollageEndOpinion = db.Column(db.Text,nullable=True)#(学院意见 结题)
    DCCenterEndOpinion = db.Column(db.Text,nullable=True)#大创中心意见（结题）
    Achievement = db.Column(db.String(220),nullable=True)#成绩
    doc = db.Column(db.String(220),nullable=True)#结题成果
    linku = db.relationship('User_Project',backref='project')
    files = db.relationship('File',backref='file')
    def getPid(self,Pname):
        return self.query.filter_by(Pname=Pname).first().pid

    def __repr__(self):
        return  '<Project %r>'%self.pid

class File(db.Model):
    __tablename__ = 'File'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(220),nullable=True)
    project_id = db.Column(db.Integer,db.ForeignKey('project.pid'))
    def __repr__(self):
        return  '<file %r>'%self.name

class ForTeacher(db.Model):
    __tablename__ = 'ForTeacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220),nullable=True)
    title = db.Column(db.String(220),nullable=True)
    company = db.Column(db.String(220),nullable=True)
    tel = db.Column(db.String(220),nullable=True)
    email = db.Column(db.String(220),nullable=True)
    projects = db.relationship('Project',backref = 'ForTeacher')



# 项目状态
class Project_mode(db.Model):
        __tablename__ = 'Project_mode'
        sid = db.Column(db.Integer, primary_key=True)
        status = db.Column(db.String(220), unique=True)


#获奖级别
class AwardLevel(db.Model):
    __tablename__ = 'AwardLevel'
    ALid = db.Column(db.Integer, primary_key=True)
    ALname = db.Column(db.String(220), unique=True)
    Competition = db.relationship('Competition',backref='Cawardlevel')
#获奖等级
class AwardGrade(db.Model):
    __tablename__ = 'AwardGrade'
    AGid = db.Column(db.Integer, primary_key=True)
    AGname = db.Column(db.String(220), unique=True)
    Competition = db.relationship('Competition',backref='CawardGrade')
#竞赛类别
class CompetitionClass(db.Model):
    __tablename__ = 'CompetitionClass'
    CCid = db.Column(db.Integer, primary_key=True)
    CCname = db.Column(db.String(220), unique=True)
    Competition = db.relationship('Competition',backref='Cclass')

#竞赛
class Competition(db.Model):
    __tablename__ = 'Competition'
    Cid = db.Column(db.Integer, primary_key=True)
    Cname = db.Column(db.String(220), unique=True)#竞赛名称
    Cclass_id = db.Column(db.Integer,db.ForeignKey('CompetitionClass.CCid'))#竞赛类别id
    Field = db.Column(db.String(220), nullable=True)#领域
    Works = db.Column(db.String(220), nullable=True)#获奖作品
    Cawardlevel_id = db.Column(db.Integer,db.ForeignKey('AwardLevel.ALid'))#获奖级别
    Cawardgrade_id = db.Column(db.Integer,db.ForeignKey('AwardGrade.AGid'))#获奖等级
    AwardClass = db.Column(db.String(220), nullable=True)#获奖类别
    Sponsor = db.Column(db.String(220), nullable=True)#主办单位
    Teacher = db.Column(db.String(220), nullable=True)#指导教师
    TeacherCollage = db.Column(db.String(220), nullable=True)#指导教师所属单位
    Remarks = db.Column(db.String(220), nullable=True)#备注
    AwardTime = db.Column(db.String(220), nullable=True)#获奖时间
    Auth = db.Column(db.String(220), nullable=True)#竞赛是否获得了审核
    AwardAuth = db.Column(db.String(220), nullable=True)#竞赛获奖情况是否获得了审核

    def __repr__(self):
        return '<Competition %r>' % self.Cname


#资金
class Funds(db.Model):
    __tablename__ = "funds"
    Fid = db.Column(db.Integer,primary_key=True)
    FundingUse = db.Column(db.Text)
    Amount = db.Column(db.Integer)
    Pid = db.Column(db.Integer)

#成果形式
class ResultsType(db.Model):
    __tablename__ = "ResultsType"
    Rid = db.Column(db.Integer,primary_key=True)
    Rname = db.Column(db.String(64))

#成果，专利
class Patent(db.Model):
    __tablename__ = "patent"
    patentId = db.Column(db.Integer,primary_key=True)
    patentName = db.Column(db.String(220))
    person = db.Column(db.String(220))
    number = db.Column(db.String(220))
    remarks = db.Column(db.String(220))
#成果，论文
class Paper(db.Model):
    __tablename__ = "paper"
    paperId = db.Column(db.Integer,primary_key=True)
    subject = db.Column(db.String(220))
    author = db.Column(db.String(220))
    JournalName = db.Column(db.String(220))
    remarks = db.Column(db.String(220))
#成果，报告
class Report(db.Model):
    __tablename__ = "report"
    reportId = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(220))
    author = db.Column(db.String(220))
    remarks = db.Column(db.String(220))
#成果，商业计划书
class BusinessPlan(db.Model):
    __tablename__ = "BusinessPlan"
    BusinessPlanId = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(220))
    remarks = db.Column(db.String(220))
#成果，网站
class Website(db.Model):
    __tablename__="Website"
    WebId = db.Column(db.Integer,primary_key=True)
    website = db.Column(db.String(220))
    remarks = db.Column(db.String(220))
#成果，其他
class Other(db.Model):
    __tablename__ = "other"
    OtherId = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(220))
    remarks = db.Column(db.String(220))



#表单

#上传文件表单
class UploadForm(Form):
    file = FileField("选择要上传的文件")
    submit = SubmitField('上传')
#中期申报表单
class ProjectMid(Form):
    MidProgress = TextAreaField("研究工作进展情况")
    file = FileField("提交成果物")
    submit = SubmitField('提交')

#结题报告表单
class ProjectEnd(Form):
    ResultsDescribe = TextAreaField("项目成果简介")
    ResultsSummary = TextAreaField("项目总结报告")
    Problems = TextAreaField("项目遇到的问题和建议")
    file = FileField("提交成果物")
    submit = SubmitField('提交')


#加入项目页面的表单
class Join_project(Form):
    projectname = StringField("项目名")
    submit = SubmitField('加入')

#小工具
#判断是否为空字符串
def isSpaceStr(srr):
    if srr == '':
        return None
    else:
        return srr

#根据 user_id 找到对应的 user, 如果没有找到，返回None, 此时的 user_id 将会自动从 session 中移除, 若能找到 user ，则 user_id 会被继续保存.
@login_manager.user_loader
def load_user(user_id):
    """Load the user's info."""
    return User.query.filter_by(id=user_id).first()
#判断是否提交了项目成员数据，提交了就添加一个新用户
def addProUser():
    pass
#根据用户名生成一个由项目构成的列表（项目是数据库一行记录的映射）
def findMyproject(username):
    try:
        Userid = User.query.filter_by(username=username).first().userid
        Pid = User_Project.query.filter_by(userid=Userid).all()
        pidlist = [x.pid for x in Pid]
        Prolist = [Project.query.filter_by(pid=x).first() for x in pidlist]
        return Prolist
    except:
        return '发生了未知错误，请联系管理员，感谢您的支持<findMyproject>'

#生成一个由状态号和状态名组成的元组构成的列表
def createStatuslist():
    a = [(x.sid, x.status) for x in Project_mode.query.all()]
    return a

#根据提供的用户名获取用户现在的权限
def getUserauth(user):
   return User.query.filter_by(username=user).first().usermode
#根据状态名获取项目状态号
def getProStatusSid(status):
    return Project_mode.query.filter_by(status=status).first().sid

#路由
@app.route('/')
def index():
    return render_template('index.html')

#管理页面
@app.route('/projectManage-manager.html')
def projectManage():
    username=session["username"]
    page = request.args.get('page', 1, type=int)
    if User_mode.query.filter_by(mid=getUserauth(username)).first().name == '管理员':
        pagination = Project.query.filter_by().paginate(page, per_page=10, error_out=False)
        pros = pagination.items
        return render_template('/manager/projectManage-manager.html',pros=pros,stalist=createStatuslist(),pagination=pagination)
    elif User_mode.query.filter_by(mid=getUserauth(username)).first().name == '学院管理员':
        pagination = Project.query.filter_by(Collage=User.query.filter_by(username=username).first().collage).paginate(page, per_page=10, error_out=False)
        pros = pagination.items
        return render_template('/manager/projectManage-manager.html', pros=pros,stalist=createStatuslist(),pagination=pagination)
    elif User_mode.query.filter_by(mid=getUserauth(username)).first().name == '教师用户':
        pagination = Project.query.filter_by(Teacher=User.query.filter_by(username=username).first().username).paginate(page, per_page=10, error_out=False)
        pros = pagination.items
        return render_template('/manager/projectManage-manager.html', pros=pros,stalist=createStatuslist(),pagination=pagination)
#完成登录功能
@app.route('/login',methods=['GET'])
def login1():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login2():
    username = User.query.filter_by(username=request.form.get('username')).first()
    try:
        if username:
            if username.password == request.form.get('password'):
                session["username"] = username.username
                # 判断用户类型
                if username.usermode == User_mode.query.filter_by(name='学生').first().mid:
                    return render_template('loginsucc-student.html', name=username.name,
                                           pros=findMyproject(username=session['username']), stalist=createStatuslist())
                elif username.usermode == User_mode.query.filter_by(name='管理员').first().mid:
                    return render_template('Manager.html', name=username.name, type=1)
                elif username.usermode == User_mode.query.filter_by(name='学院管理员').first().mid:
                    return render_template('Manager.html', name=username.name, type=2)
                elif username.usermode == User_mode.query.filter_by(name='教师用户').first().mid:
                    return render_template('Manager.html', name=username.name, type=3)

            else:
                return render_template('loginfail.html')
        else:
            return render_template('loginfail.html')
    except:
        return '发生了未知错误，请联系管理员'




@app.route('/home-manager.html')
def home_manager():
    return  render_template('home-manager.html')

#我的项目
@app.route('/myproject')
def myproject():
    return render_template('myproject.html',pros=findMyproject(username=session['username']),stalist=createStatuslist(),user=User.query.filter_by(username=session['username']).first(),users=User,int = int)

#完成注册功能
@app.route('/register',methods=['GET'])
def register1():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register2():
    username = User.query.filter_by(username=request.form.get('username')).first()
    try:
        if username is  None:
            user = User()
            user.username = request.form.get('username')
            user.name = request.form.get('name')
            user.password = request.form.get('password')
            user.collage = request.form.get('collage')
            user.major = request.form.get('major')
            user.tel = request.form.get('tel')
            user.email = request.form.get('email')
            user.usermode = User_mode.query.filter_by(name='学生').first().mid

            db.session.add(user)
            db.session.commit()
            return render_template("registersucc.html")
        else:
            return render_template('registerfail.html')
    except:
        return '发生了一些错误，请联系管理员，感谢您的支持'

#完成创建项目功能
#项目申报
@app.route('/project_application.html',methods=['GET'])
def project_application():
    return render_template('project_application.html')

@app.route('/project_application_content.html',methods=['GET'])
def project_application_content1():
    return render_template('project_application_content.html')

@app.route('/project_application_content.html', methods=['POST'])
def project_application_content2():
    #try:
        pname = Project.query.filter_by(Pname=request.form.get('Pname')).first()
        fortea = ForTeacher()
        if request.form.get('forname') != '':
            fortea.name = request.form.get('forname')
            fortea.title = request.form.get('fortitle')
            fortea.email = request.form.get('foremail')
            fortea.company = request.form.get('forcompany')
            fortea.tel = request.form.get('fortel')
            db.session.add(fortea)
            db.session.commit()
        if pname is None:
            pro = Project()
            pro.StartDate = datetime.datetime.now().strftime('%Y/%m/%d')
            pro.Pname = isSpaceStr(request.form.get('Pname'))
            pro.PlanDate = isSpaceStr(request.form.get('PlanDate'))
            pro.Status = Project_mode.query.filter_by(status='等待指导教师审核').first().sid
            pro.Collage = isSpaceStr(request.form.get('Collage'))
            pro.Teacher = request.form.get('Teacher')
            pro.secondTeacher = request.form.get('secondTeacher')
            pro.proID = request.form.get('proID')
            pro.Describe = isSpaceStr(request.form.get('Describe'))
            pro.Pclass = isSpaceStr(request.form.get('Pclass'))
            pro.ReassonsForApplication = isSpaceStr(request.form.get('ReassonsForApplication'))
            pro.ProjectPlan = isSpaceStr(request.form.get('ProjectPlan'))
            pro.Innovate = isSpaceStr(request.form.get('Innovate'))
            pro.Schedule = isSpaceStr(request.form.get('Schedule'))
            pro.Budget = isSpaceStr(request.form.get('Budget'))
            pro.BudgetPlan = isSpaceStr(request.form.get('BudgetPlan'))
            pro.ExpectedResults = isSpaceStr(request.form.get('ExpectedResults'))
            pro.Person_in_charge = session["username"]
            if request.form.get('forname') != '':
                pro.ForTeacher_ID=ForTeacher.query.filter_by(name = request.form.get('forname')).first().id
            db.session.add(pro)
            db.session.commit()
            pu = User_Project()
            pu.pid=Project.query.filter_by(Pname=request.form.get('Pname')).first().pid
            pu.userid=User.query.filter_by(username=Project.query.filter_by(Pname=request.form.get('Pname')).first().Person_in_charge).first().userid
            db.session.add(pu)
            db.session.commit()
            for x in [1, 2, 3, 4]:
                try:
                    if request.form.get('username'+str(x)):
                        isuser = User.query.filter_by(username=request.form.get('username' + str(x))).first()
                        if isuser is None:
                            users = User()
                            users.username = request.form.get('username' + str(x))
                            users.password = '123456'
                            users.name = request.form.get('name' + str(x))
                            users.collage = request.form.get('collage'+str(x))
                            users.major = request.form.get('major'+str(x))
                            users.tel = request.form.get('tel'+str(x))
                            users.email = request.form.get('email'+str(x))
                            users.usermode = User_mode.query.filter_by(name='学生').first().mid
                            db.session.add(users)
                            db.session.commit()
                        pub = User_Project.query.filter_by(pid=Project.query.filter_by(Pname=request.form.get('Pname')).first().pid,userid=User.query.filter_by(username=request.form.get('username'+ str(x))).first().userid).first()
                        if pub is None:
                            db.session.add(User_Project(pid=Project.query.filter_by(Pname=request.form.get('Pname')).first().pid,
                                           userid=User.query.filter_by(username=request.form.get('username'+ str(x))).first().userid))
                            db.session.commit()

                except:
                    db.session.close_all()
                    return '添加学生到项目发生了错误,请重试'
            """
            file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
            if not os.path.exists(file_dir)
                os.makedirs(file_dir)
            # 重命名文件
            file = request.files['file']
            fname = secure_filename(file.filename).split('.', 1)[-1]
            new_filename = str(pro.pid) + 'Star' + '.' + fname
            file.save(file_dir,new_filename)
            """
            return '创建成功'
        else:
            return "项目已存在"
   # except:
    #    return '出现了一些错误，请重试'
#中期申报

@app.route('/interim_report.html',methods=['GET'])
def interim_report():
    return render_template('interim_report.html')


@app.route('/interim_report_content.html',methods=['GET'])
def interim_report_content1():
    return render_template('interim_report_content.html')

@app.route('/interim_report_content.html',methods=['POST'])
def interim_report_content():
    pro = Project.query.filter_by(pid=session['project']).first()
    pro.MidProgress = request.form.get('MidProgress')
    pro.Status = Project_mode.query.filter_by(status='等待指导教师中期审核').first().sid
    db.session.add(pro)
    db.session.commit()
    return '提交成功'
"""
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # 重命名文件
    fname = secure_filename(form.file.data.filename).split('.', 1)[-1]
    unix_time = int(time.time())
    new_filename = str(pro.pid) + 'Mid' + '.' + fname

    form.file.data.save('upload/' + new_filename)
    pro.MidResults = new_filename
    """


#结题报告
@app.route('/concluding_report.html',methods=['GET'])
def concluding_report():
    return render_template('concluding_report.html')
@app.route('/concluding_report_content.html',methods=['GET'])
def concluding_report_content1():
    return render_template('concluding_report_content.html')
@app.route('/concluding_report_content.html',methods=['POST'])
def concluding_report_content():
    pro = Project.query.filter_by(pid=session['project']).first()
    pro.ResultsDescribe = request.form.get('ResultsDescribe')
    pro.ResultsSummary = request.form.get('ResultsSummary')
    pro.Problems = request.form.get('Problems')
    """
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # 重命名文件
    fname = secure_filename(form.file.data.filename).split('.', 1)[-1]
    new_filename = str(pro.pid)+'End'+ '.' + fname

    form.file.data.save('upload/'+ new_filename)
    pro.doc = new_filename
    """
    pro.Status = Project_mode.query.filter_by(status='等待指导教师结题审核').first().sid
    db.session.add(pro)
    db.session.commit()
    return '提交成功'
#上传文件路由
@app.route('/upload/<pid>',methods=['GET','POST'])
def upload(pid):
    form=UploadForm()
    if form.validate_on_submit():
        a=File()
        a.name=form.file.data.filename
        a.project_id=pid
        form.file.data.save('/upload/'+a.name)
        db.session.add(a)
        db.session.commit()
        return '上传成功'
    return render_template('upload.html',form=form)

#创建学院管理员账号
@app.route('/addCollageAdminUser.html',methods=['GET'])
def addCollageAdminUser1():
    return render_template('addCollageAdminUser.html')
@app.route('/addCollageAdminUser.html',methods=['POST'])
def addCollageAdminUser2():
    username = User.query.filter_by(username=request.form.get('username')).first()
    if username is None:
        user = User()
        user.username = request.form.get('username')
        user.password = '123456'
        user.collage = request.form.get('collage')
        user.usermode = User_mode.query.filter_by(name='学院管理员').first().mid
        db.session.add(user)
        db.session.commit()
        return render_template("registersucc.html")
    else:
        return render_template('registerfail.html')

#管理学院管理员页面
@app.route('/CollageAdminUser.html',methods=['GET'])
def CollageAdminUser():
    collageUser = User.query.filter_by(usermode = 4).all()
    return render_template('CollageAdminUser.html',collageUser = collageUser)
#管理教师用户页面
@app.route('/teacherUser.html',methods=['GET'])
def teacherUser():
    teacherUser = User.query.filter_by(usermode = 3,collage=User.query.filter_by(username=session['username']).first().collage).all()
    return render_template('TeacherUser.html',teacherUser = teacherUser)

#创建教师用户
@app.route('/addTeacherUser.html',methods=['GET'])
def addTeacherUser1():
    return render_template('addTeacherUser.html')

@app.route('/addTeacherUser.html',methods=['POST'])
def addTeacherUser2():
    username = User.query.filter_by(username=request.form.get('username')).first()
    if username is None:
        user = User()
        user.username = request.form.get('username')
        user.name = request.form.get('name')
        user.password = '123456'
        user.collage = request.form.get('collage')
        user.usermode = User_mode.query.filter_by(name='教师用户').first().mid
        db.session.add(user)
        db.session.commit()
        return render_template("registersucc.html")
    else:
        return render_template('registerfail.html')


#完成用户加入项目功能
@app.route('/join_project.html',methods=['GET'])
def join_project1():
    return render_template('join_project.html')
@app.route('/join_project.html',methods=['POST'])
def join_project2():
    try:
        pud = User_Project.query.filter_by(pid=Project.query.filter_by(Pname=request.form.get('Pname')).first().pid,userid=User.query.filter_by(username=session["username"]).first().userid).first()
        pro = Project.query.filter_by(Pname=request.form.get('Pname')).first()
        if pud is None:
            if pro is not None:
                pu = User_Project()
                pu.userid = User.query.filter_by(username=session["username"]).first().userid
                pu.pid = Project.query.filter_by(Pname=request.form.get('Pname')).first().pid
                db.session.add(pu)
                db.session.commit()
                return '加入成功'
            else:
                return '您要加入的项目不存在，请确认项目名称后重试'
        else:
            return '您已经加入了项目'
    except:
        return '您要加入的项目不存在，请确认项目名称后重试'
#删除项目成员路由
@app.route('/delete/members/<userid>')
def deleteMembers(userid):
    pud = User_Project.query.filter_by(pid=session['project'],userid=userid).first()
    db.session.delete(pud)
    db.session.commit()
    return '删除成功'





#竞赛申报
@app.route('/Competition_declaration.html',methods=['GET'])
def Competition_declaration1():
    return render_template('Competition_declaration.html')
@app.route('/Competition_declaration.html',methods=['POST'])
def Competition_declaration():
    Cname = Competition.query.filter_by(Cname=request.form.get('Cname')).first()
    try:
        if Cname is None:
            com = Competition()
            com.Cname = request.form.get('Cname')
            com.Sponsor = request.form.get('Sponsor')
            com.Field = request.form.get('Field')
            com.Remarks = request.form.get('Remarks')
            com.Auth = '未审核'
            db.session.add(com)
            db.session.commit()
            return '竞赛申报成功'
        else:
            return '竞赛申报失败'
    except:
        return '发生未知错误，请联系管理员,感谢您的支持'

#竞赛管理页面
@app.route('/CompetitionManager')
def CompetitionManager():
    if User.query.filter_by(username=session['username']).first().mode.name == '管理员':
        page = request.args.get('page', 1, type=int)
        pagination = Competition.query.filter_by().paginate(page, per_page=10, error_out=False)
        pros = pagination.items
        return render_template('/manager/CompetitionManager.html', pros=pros, pagination=pagination)
    else:
        return '只允许管理员访问该页面'
#审核竞赛路由
@app.route('/authCom/<Cid>')
def authCom(Cid):
    a=Competition.query.filter_by(Cid=Cid).first()
    a.Auth = '已审核'
    db.session.add(a)
    db.session.commit()
    return '审核成功'

#删除竞赛路由
@app.route('/delete/<Cid>')
def deleteCom(Cid):
    db.session.delete(Competition.query.filter_by(Cid=Cid).first())
    db.session.commit()
    return '删除成功'

#参加竞赛路由
@app.route('/joinCom/<Cid>')
def joinCom(Cid):
    user = User.query.filter_by(username=session['username']).first()
    user.Competitions.append(Competition.query.filter_by(Cid=Cid).first())
    db.session.add(user)
    db.session.commit()
#创建参赛队伍
@app.route('/createComTeam/<com>',methods=['GET'])
def createComTeam(com):
    return render_template('createComTeam.html',com=com)
@app.route('/createComTeam/<com>',methods=['POST'])
def createComTeam1(com):
    users = request.form.get('users').split(',')
    coms = Competition.query.filter_by(Cid=com).first()
    if coms.Teacher is None:
        for x in users:
            a=User.query.filter_by(username=x).first()
            a.Competitions.append(coms)
            db.session.add(a)
            db.session.commit()
        coms.Teacher = session['username']
        coms.TeacherCollage = User.query.filter_by(username=session['username']).first().collage
        db.session.add(coms)
        db.session.commit()
        return '创建竞赛队伍成功'
    else:
        return '已经有参赛队伍了'
#教师竞赛列表
@app.route('/teacherComList.html')
def teacherComList():
    if User.query.filter_by(username=session['username']).first().mode.name == '教师用户':
        page = request.args.get('page', 1, type=int)
        pagination = Competition.query.filter_by(Auth='已审核').paginate(page, per_page=10, error_out=False)
        pros = pagination.items
        return render_template('/teacherComList.html', pros=pros, pagination=pagination)
    else:
        return '只允许教师用户访问该页面'


#项目内容路由
@app.route('/project/<pid>')
def project(pid):
  #  try:
        auth = None
        mid = None
        end = None
        pro = Project.query.filter_by(pid=pid).first()
        session['project'] = pid
        pchar = User.query.filter_by(username=Project.query.filter_by(pid=pid).first().Person_in_charge).first()
        pmembers = [User.query.filter_by(userid=x.userid).first() for x in User_Project.query.filter_by(pid=pid).all()]
        teacher = User.query.filter_by(username=Project.query.filter_by(pid=pid).first().Teacher).first()
        secondTeacher = User.query.filter_by(username=Project.query.filter_by(pid=pid).first().secondTeacher).first()
        # 生成用来判断是否显示按钮的变量
        if User_mode.query.filter_by(mid=getUserauth(session['username'])).first().name == '管理员' and pro.Status in [3,7,11]:
            auth = True
        elif User_mode.query.filter_by(mid=getUserauth(session['username'])).first().name == '学院管理员' and pro.Status in [2, 6, 10]:
            auth = True
        elif User_mode.query.filter_by(mid=getUserauth(session['username'])).first().name == '教师用户' and pro.Status in [1, 5, 9]:
            auth = True
        if pro.Status == 4:
            mid = True
        if pro.Status == 8:
            end = True
        psta = None
        for x in createStatuslist():  # 生成用来判断显示什么按钮的变量
            if pro.Status == x[0]:
                psta = (x[0], x[1])  # x[0]为状态号，x[1]为状态名
        return render_template('project.html', pro=pro, pchar=pchar, pmembers=pmembers, auth=auth, pstatus=psta,mid=mid, end=end, teacher=teacher,secondTeacher=secondTeacher,user=User.query.filter_by(username=session['username']).first())
   # except:
    #    return '发生了未知错误，请联系管理员，感谢您的支持'

#完成项目审核和路由
@app.route('/check-suggest.html')
def check_suggest():
    return render_template('check-suggest.html',pro=Project.query.filter_by(pid=session['project']).first())
@app.route('/auth/<yesno>',methods=['POST'])
def authyes(yesno):
    try:
        info = None
        pro = Project.query.filter_by(pid=session['project']).first()
        if yesno == 'succ':
            info = '审核成功'
            if pro.Status == 1:
                pro.TeaStarOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 2:
                pro.CollStarOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 3:
                pro.SchStarOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 5:
                pro.TeaMidOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 6:
                pro.SchMidOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 7:
                pro.DCCenterMidOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 9:
                pro.TeaEndOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 10:
                pro.CollageEndOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 11:
                pro.DCCenterEndOpinion = isSpaceStr(request.form.get('opinion'))
            pro.Status = pro.Status + 1
            db.session.add(pro)
            db.session.commit()
            return render_template('authsucc.html', info=info)
        elif yesno == 'fail':
            if pro.Status == 1:
                pro.TeaStarOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 2:
                pro.CollStarOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 3:
                pro.SchStarOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 5:
                pro.TeaMidOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 6:
                pro.SchMidOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 7:
                pro.DCCenterMidOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 9:
                pro.TeaEndOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 10:
                pro.CollageEndOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status == 11:
                pro.DCCenterEndOpinion = isSpaceStr(request.form.get('opinion'))
            if pro.Status in [1, 2, 3]:
                pro.Status = 13
            elif pro.Status in [5, 6, 7]:
                pro.Status = 14
            elif pro.Status in [9, 10, 11]:
                pro.Status = 15
            db.session.add(pro)
            db.session.commit()
            info = '审核不通过成功'
            return render_template('authsucc.html', info=info)
    except:
        return '发生了未知错误，请联系管理员，感谢您的支持'


#下载文件路由
@app.route('/download/<filename>', methods=['GET'])
def startdownload(filename):
    response = make_response(send_file("/upload/"+filename))
    response.headers["Content-Disposition"] = "attachment; filename="+filename+";"
    return response


#删除用户路由
@app.route('/delete/user/<username>',methods=['GET'])
#根据用户名删除数据库中的用户
def deleteUser(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return render_template('deleteUserSucc.html')

#修改个人信息
@app.route('/updatecollageAdminInfo.html',methods=['GET'])
def updatecollageAdminInfo1():
    user = User.query.filter_by(username=session['username']).first()
    return render_template('updatecollageAdminInfo.html',userinfo=user)

@app.route('/updatecollageAdminInfo.html', methods=['POST'])
def updatecollageAdminInfo2():
    try:
        user = User.query.filter_by(username=session['username']).first()
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.tel = request.form.get('tel')
        db.session.add(user)
        db.session.commit()
        return render_template('changeUserInfoSucc.html')
    except:
        return '发生了未知错误，请联系管理员，感谢您的支持'

#修改教师个人信息
@app.route('/updatePersonalTeacherInfo.html',methods=['GET'])
def updatePersonalTeacherInfo1():
    user = User.query.filter_by(username=session['username']).first()
    return render_template('/updatePersonalTeacherInfo.html',userinfo=user)

@app.route('/updatePersonalTeacherInfo.html', methods=['POST'])
def updatePersonalTeacherInfo2():
    try:
        user = User.query.filter_by(username=session['username']).first()
        user.name = request.form.get('name')
        user.collage = request.form.get('collage')
        user.email = request.form.get('email')
        user.tel = request.form.get('tel')
        db.session.add(user)
        db.session.commit()
        return render_template('changeUserInfoSucc.html')
    except:
        return '发生了未知错误，请联系管理员，感谢您的支持'

@app.route('/updateStudentInfo.html',methods=['GET'])
def updateStudentInfo1():
    return render_template('updateStudentInfo.html',userinfo = User.query.filter_by(username=session['username']).first())
@app.route('/updateStudentInfo.html',methods=['POST'])
def updateStudentInfo2():
    try:
        user = User.query.filter_by(username=session['username']).first()
        user.email = request.form.get('email')
        user.tel = request.form.get('tel')
        user.name = request.form.get('name')
        user.collage = request.form.get('collage')
        user.major = request.form.get('major')
        db.session.add(user)
        db.session.commit()
        return render_template('changeUserInfoSucc.html')
    except:
        return '发生了未知错误，请联系管理员，感谢您的支持'

#删除项目路由
@app.route('/delete/project/<pid>')
def deletePro(pid):
    try:
        pro = Project.query.filter_by(pid=pid).first()
        pu = User_Project.query.filter_by(pid=pid).all()
        db.session.delete(pro)
        db.session.commit()
        for x in pu:
            db.session.delete(x)
            db.session.commit()
        return render_template('deleteUserSucc.html')
    except:
        return '发生了未知错误，请联系管理员，感谢您的支持'

#确认删除
@app.route('/secondConfirmation/<pid>')
def secondConfirmation(pid):
    return render_template('secondConfirmation.html',pid=pid)

#修改密码路由
@app.route('/updatePassword.html',methods=['GET'])
def updatePassword():
    return render_template('updatePassword.html')
@app.route('/change/password',methods=['POST'])
def changePassword():
    user = User.query.filter_by(username = session['username']).first()
    password=request.form.get('password')
    repassword = request.form.get('repassword')
    if password == repassword :
        user.password = repassword
    else:
        return '两次输入密码不通，请重试'
    db.session.add(user)
    db.session.commit()
    return "密码修改成功"

#找回密码
@app.route('/findPassword',methods=['GET'])
def findPassword():
    return render_template('findPassword.html')
@app.route('/findPassword',methods=['POST'])
def findPassword1():
    username = request.form.get('username')
    email = request.form.get('email')
    user = User.query.filter_by(username=username).first()
    if user.email ==email:
        user.password = '123456'
        db.session.add(user)
        db.session.commit()
        return render_template('resetPasswordSucc.html')
    else:
        '您输入的信息有误，无法找回密码'
#重置初始密码
@app.route('/resetPassword/<username>')
def resetPassword(username):
    user = User.query.filter_by(username=username).first()
    user.password='123456'
    db.session.add(user)
    db.session.commit()
    return render_template('resetPasswordSucc.html')
#查看个人信息路由
@app.route('/checkStudentInfo.html')
def checkStudentInfo():
    return render_template('checkStudentInfo.html',userinfo=User.query.filter_by(username=session['username']).first())

@app.route('/search.html',methods=['GET'])
def search():
    return render_template('search.html')
@app.route('/search.html',methods=['POST'])
def search1():
    pro = Project.query.filter_by(proID=request.form.get('proID')).first()
    if pro is not None:
        return render_template('/project/'+int(pro.pid))
    else:
        return '您搜索的项目不存在'

@app.route('/loginout.html',methods=['GET'])
def loginout():
    session['username']=None
    return render_template('index.html')

if __name__ == '__main__':
    manager.run()