#-*- encoding:utf-8 -*-
from hello import AwardLevel,db
db.session.add(AwardLevel(ALname='省级A类'))
db.session.add(AwardLevel(ALname='省级B类'))
db.session.add(AwardLevel(ALname='国家级A类'))
db.session.add(AwardLevel(ALname='国家级B类'))
db.session.add(AwardLevel(ALname='国家级C类'))
db.session.add(AwardLevel(ALname='国际级'))
db.session.commit()
