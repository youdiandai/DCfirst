#-*- encoding:utf-8 -*-
from . import db

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
    PlanDate = db.Column(db.String(64),nullable=True)#项目周期
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
