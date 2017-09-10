#-*- encoding:utf-8 -*-
from hello import AwardGrade,db
db.session.add(AwardGrade(AGname='三等奖'))
db.session.add(AwardGrade(AGname='二等奖'))
db.session.add(AwardGrade(AGname='一等奖'))
db.session.add(AwardGrade(AGname='特等奖'))
db.session.commit()
