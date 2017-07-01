#-*- encoding:utf-8 -*-
from hello import Collage,db
f= open('collage.txt')
for x in f:
 db.session.add(Collage(cname=x[:-1]))
db.session.commit()