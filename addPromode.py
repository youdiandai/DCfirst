#-*- encoding:utf-8 -*-
from hello import db,Project_mode
db.session.add(Project_mode(status='δ���'))
db.session.add(Project_mode(status='δ���'))
db.session.add(Project_mode(status='���'))
db.session.add(Project_mode(status='���δͨ��'))
db.session.commit()