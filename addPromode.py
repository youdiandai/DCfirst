#-*- encoding:utf-8 -*-
from hello import db,Project_mode
db.session.add(Project_mode(status='未审核'))
db.session.add(Project_mode(status='未完成'))
db.session.add(Project_mode(status='审核未通过'))
db.session.add(Project_mode(status='完成'))
db.session.commit()