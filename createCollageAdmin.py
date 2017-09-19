#-*- encoding:utf-8 -*-
from hello import db,User
f=open('danwei.txt','rt',encoding="utf-8")
for x in f:
    db.session.add(User(username=x.split(',')[1][:-1],collage=x.split(',')[0],password='123456',usermode=4))
db.session.commit()