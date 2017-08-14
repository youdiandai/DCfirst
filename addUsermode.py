#-*- encoding:utf-8 -*-
from hello import User_mode,db
judge = User_mode(name='学生')
manager = User_mode(name='管理员')
student = User_mode(name='教师用户')
proleader = User_mode(name='学院管理员')
db.session.add(judge)
db.session.add(manager)
db.session.add(student)
db.session.add(proleader)
db.session.commit()
