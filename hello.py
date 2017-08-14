#-*- encoding:utf-8 -*-
from flask import Flask,render_template,session,make_response,send_file,request
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,RadioField,TextAreaField,SelectField,FileField
from wtforms.validators import DataRequired,equal_to,Email
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
    name = db.Column(db.String(64),nullable=False)
    password = db.Column(db.String(64),nullable=False)
    collage = db.Column(db.String(64), nullable=True)
    major = db.Column(db.String(64), nullable=True)
    tel = db.Column(db.String(64),nullable=True)
    email = db.Column(db.String(64),nullable=True)
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
    pid = db.Column(db.Integer,primary_key=True)#项目编号
    Pname = db.Column(db.String(64),nullable=False)#项目名称
    Plevel = db.Column(db.String(64),nullable=True)#项目级别
    Pclass = db.Column(db.String(64),nullable=True)#项目类别
    Collage = db.Column(db.String(64),nullable=True)#学院
    Person_in_charge = db.Column(db.Integer,nullable=True)#负责人
    Teacher = db.Column(db.String(64),nullable=True)#指导教师
    Forteacher = db.Column(db.String(64),nullable=True)#校外导师
    Describe = db.Column(db.Text,nullable=True)#项目简介
    Status = db.Column(db.Integer,nullable=True)#项目状态
    StartDate = db.Column(db.String(64),nullable=True)#立项日期
    PlanDate = db.Column(db.String(64),nullable=True)#预计结束日期
    MidSubdate = db.Column(db.String(64),nullable=True)#中期报告提交日期
    EndSubdate = db.Column(db.String(64),nullable=True)#结题提交日期
    EndDate = db.Column(db.String(64),nullable=True)#项目结束日期
    ReassonsForApplication = db.Column(db.String(64),nullable=True)#申请理由
    ProjectPlan = db.Column(db.String(64),nullable=True)#项目方案
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
    TeaMidOpinion = db.Column(db.Text,nullable=True)#指导教师意见（中期）
    DCCenterMidOpinion = db.Column(db.Text,nullable=True)#大创中心意见（中期）
    SchMidOpinion = db.Column(db.Text,nullable=True)#学校意见（中期）
    ResultsDescribe = db.Column(db.Text,nullable=True)#项目成果简介
    ResultsType = db.Column(db.Integer,nullable=True)#项目成果形式
    ResultsSummary = db.Column(db.Text,nullable=True)#项目总结报告
    ResultsNum = db.Column(db.Integer,nullable=True)#成果编号
    Problems = db.Column(db.Text,nullable=True)#存在的问题和建议
    TeaEndOpinion = db.Column(db.Text,nullable=True)#项目指导教师意见（结题）
    DCCenterEndOpinion = db.Column(db.Text,nullable=True)#大创中心意见（结题）
    Achievement = db.Column(db.String(64),nullable=True)#成绩
    doc = db.Column(db.String(64),nullable=True)#结题成果
    linku = db.relationship('User_Project',backref='project')
    def __repr__(self):
        return  '<Project %r>'%self.pid

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
    patentName = db.Column(db.String(64))
    person = db.Column(db.String(64))
    number = db.Column(db.String(64))
    remarks = db.Column(db.String(64))
#成果，论文
class Paper(db.Model):
    __tablename__ = "paper"
    paperId = db.Column(db.Integer,primary_key=True)
    subject = db.Column(db.String(64))
    author = db.Column(db.String(64))
    JournalName = db.Column(db.String(64))
    remarks = db.Column(db.String(64))
#成果，报告
class Report(db.Model):
    __tablename__ = "report"
    reportId = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    author = db.Column(db.String(64))
    remarks = db.Column(db.String(64))
#成果，商业计划书
class BusinessPlan(db.Model):
    __tablename__ = "BusinessPlan"
    BusinessPlanId = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    remarks = db.Column(db.String(64))
#成果，网站
class Website(db.Model):
    __tablename__="Website"
    WebId = db.Column(db.Integer,primary_key=True)
    website = db.Column(db.String(64))
    remarks = db.Column(db.String(64))
#成果，其他
class Other(db.Model):
    __tablename__ = "other"
    OtherId = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    remarks = db.Column(db.String(64))


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
    email = StringField("E-mail",validators=[Email()])
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
#立项申请
class ProjectApproval(Form):
    projectname = StringField("项目名")
    PlanDate = StringField("预计结束日期")
    member = StringField("项目成员")#中间用逗号分隔
    Teacher = StringField("指导教师")#指导教师
    collage = SelectField("项目所属学院" ,validators=[DataRequired()],choices=[(x.cname,x.cname) for x in Collage.query.all()])
    Describe = TextAreaField("项目简介")
    projectclass = RadioField('项目分类', choices=[('创新训练项目', '创新训练项目'), ('创业训练项目', '创业训练项目'),('创业实践项目', '创业实践项目')])
    ReassonsForApplication = TextAreaField("申请理由")
    ProjectPlan = TextAreaField("项目方案")
    Innovate = TextAreaField("项目特色和创新点")
    Schedule = TextAreaField("项目进度安排")
    Budget = StringField("项目经费")
    BudgetPlan = TextAreaField("经费使用计划")
    ExpectedResults = TextAreaField("项目预期成果物")
    submit = SubmitField('提交')

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

#根据状态名获取项目状态号
def getProStatusSid(status):
    return Project_mode.query.filter_by(status=status).first().sid

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
        if username.password == form.password.data:
            session["username"] = username.username
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
            user.email = register.email.data
            user.usermode = User_mode.query.filter_by(name='学生').first().mid

            db.session.add(user)
            db.session.commit()
            return render_template("registersucc.html")
        else:
            return render_template('registerfail.html')
    return render_template('register.html',form=register)

#完成创建项目功能
"""
@app.route('/createproject.html',methods=['GET','POST'])
def create_project():
    form=Create_project()
    if form.validate_on_submit():
        pname = Project.query.filter_by(Pname=form.projectname.data).first()
        if pname is None:
            #增加各种数据项到数据库
            pro = Project()
            pu=User_Project()
            pro.Pname = form.projectname.data
            pro.Plevel = form.projectlevel.data
            pro.Describe = form.describe.data
            pro.Person_in_charge=session["username"]
            pro.Collage = form.collage.data
            pro.Teacher = form.teacher.data
            pro.Status = Project_mode.query.filter_by(status='未审核').first().sid
            db.session.add(pro)
            db.session.commit()
            pu.pid=Project.query.filter_by(Pname=form.projectname.data).first().pid
            pu.userid=User.query.filter_by(username=Project.query.filter_by(Pname=form.projectname.data).first().Person_in_charge).first().userid
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
            db.session.add(pro)
            db.session.commit()
            return '创建成功'
        else:
            return '创建失败'
    return render_template('createproject.html', form=form)
"""

#项目申报
@app.route('/project_application.html',methods=['GET'])
def project_application():
    return render_template('project_application.html')

@app.route('/project_application_content.html',methods=['GET','POST'])
def project_application_content():
    form = ProjectApproval()
    if form.validate_on_submit():
        pname = Project.query.filter_by(Pname=form.projectname.data).first()
        if pname is None:
            pro = Project()
            pu = User_Project()
            pro.Pname = form.projectname.data
            pro.PlanDate = form.PlanDate.data
            pro.Status = Project_mode.query.filter_by(status='等待指导教师审核').first().sid
            pro.Collage = form.collage.data
            pro.Teacher = form.Teacher.data
            pro.Describe = form.Describe.data
            pro.Pclass = form.projectclass.data
            pro.ReassonsForApplication = form.ReassonsForApplication.data
            pro.ProjectPlan = form.ProjectPlan.data
            pro.Innovate = form.Innovate.data
            pro.Schedule = form.Schedule.data
            pro.Budget = form.Budget.data
            pro.BudgetPlan = form.BudgetPlan.data
            pro.ExpectedResults = form.ExpectedResults.data
            pro.Person_in_charge = session["username"]
            db.session.add(pro)
            db.session.commit()
            pu.pid=Project.query.filter_by(Pname=form.projectname.data).first().pid
            pu.userid=User.query.filter_by(username=Project.query.filter_by(Pname=form.projectname.data).first().Person_in_charge).first().userid
            db.session.add(pu)
            db.session.commit()
            for x in form.member.data.split(","):
                db.session.add(User_Project(pid=Project.query.filter_by(Pname=form.projectname.data).first().pid,userid=User.query.filter_by(username=x).first().userid))
                db.session.commit()
            return '创建成功'
        else:
            return "项目已存在"
    return render_template('project_application_content.html',form=form)
#中期申报
@app.route('/interim_report.html',methods=['GET'])
def interim_report():
    return render_template('interim_report.html')
@app.route('/interim_report_content.html',methods=['GET','POST'])
def interim_report_content():
    form = ProjectMid()
    if form.validate_on_submit():
        pro = Project.query.filter_by(pid=session['project']).first()
        pro.MidProgress = form.MidProgress.data

        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 重命名文件
        fname = secure_filename(form.file.data.filename).split('.', 1)[-1]
        unix_time = int(time.time())
        new_filename = pro.Pname+'Mid'+ '.' + fname

        form.file.data.save('upload/'+ new_filename)
        pro.MidResults = new_filename
        pro.Status = Project_mode.query.filter_by(status='等待指导教师中期审核').first().sid
        db.session.add(pro)
        db.session.commit()
        return '提交成功'
    return render_template('interim_report_content.html',form=form)
#结题报告
@app.route('/concluding_report.html',methods=['GET'])
def concluding_report():
    return render_template('concluding_report.html')
@app.route('/concluding_report_content.html',methods=['GET','POST'])
def concluding_report_content():
    form = ProjectEnd()
    if form.validate_on_submit():
        pro = Project.query.filter_by(pid=session['project']).first()
        pro.ResultsDescribe = form.ResultsDescribe.data
        pro.ResultsSummary = form.ResultsSummary.data
        pro.Problems = form.Problems.data
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 重命名文件
        fname = secure_filename(form.file.data.filename).split('.', 1)[-1]
        unix_time = int(time.time())
        new_filename = pro.Pname+'End'+ '.' + fname

        form.file.data.save('upload/'+ new_filename)
        pro.doc = new_filename
        pro.Status = Project_mode.query.filter_by(status='等待指导教师结题审核').first().sid
        db.session.add(pro)
        db.session.commit()
        return '提交成功'
    return render_template('concluding_report_content.html',form=form)



#完成用户加入项目功能
@app.route('/join_project',methods=['GET','POST'])
def join_project():
    form = Join_project()
    if form.validate_on_submit():
        pud = User_Project.query.filter_by(pid=Project.query.filter_by(Pname=form.projectname.data).first().pid,userid=User.query.filter_by(username=session["username"]).first().userid).first()
        if pud is None:
            pu=User_Project()
            pu.userid=User.query.filter_by(username=session["username"]).first().userid
            pu.pid=Project.query.filter_by(Pname=form.projectname.data).first().pid
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
        if pro.Status == x[0]:
            psta = (x[0],x[1]) #x[0]为状态号，x[1]为状态名
    return render_template('project.html',pro =pro ,pchar=pchar,pmembers=pmembers,auth=auth,pstatus=psta)

#完成项目审核和项目完成路由
@app.route('/auth/<num>')
def auth(num):
    info=None
    pro=Project.query.filter_by(pid=session['project']).first()
    if Project_mode.query.filter_by(sid=num).first().status == '未审核':
        pro.Status=Project_mode.query.filter_by(status='未完成').first().sid
        info='审核成功'
    elif Project_mode.query.filter_by(sid=num).first().status == '未完成':
        pro.Status=Project_mode.query.filter_by(status='完成').first().sid
        info='项目完成'
    db.session.add(pro)
    db.session.commit()
    return render_template('authsucc.html',info=info)

#下载文件路由
@app.route('/download/<filename>', methods=['GET'])
def startdownload(filename):
    response = make_response(send_file(basedir+"/upload/"+filename))
    response.headers["Content-Disposition"] = "attachment; filename="+filename+";"
    return response

if __name__ == '__main__':
    manager.run()