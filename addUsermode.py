from hello import User_mode,db
judge = User_mode(name='��ί��ʦ')
manager = User_mode(name='����Ա')
student = User_mode(name='ѧ��')
proleader = User_mode(name='��Ŀ������')
db.session.add(judge)
db.session.add(manager)
db.session.add(student)
db.session.add(proleader)
db.session.commit()