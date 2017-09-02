#-*- encoding:utf-8 -*-
from hello import db,Project_mode
pro = Project_mode.query.filter_by(status='结题').first()
if not pro:
    db.session.add(Project_mode(status='等待指导教师审核'))
    db.session.add(Project_mode(status='等待学院管理员审核'))
    db.session.add(Project_mode(status='等待大创中心审核'))
    db.session.add(Project_mode(status='待提交中期报告'))
    db.session.add(Project_mode(status='等待指导教师中期审核'))
    db.session.add(Project_mode(status='等待学院中期审核'))
    db.session.add(Project_mode(status='等待大创中心中期审核'))
    db.session.add(Project_mode(status='待提交结题报告'))
    db.session.add(Project_mode(status='等待指导教师结题审核'))
    db.session.add(Project_mode(status='等待学院结题审核'))
    db.session.add(Project_mode(status='等待大创中心结题审核'))
    db.session.add(Project_mode(status='结题'))
    db.session.commit()
pro = Project_mode.query.filter_by(status='结题审核失败').first()
if not pro:
    db.session.add(Project_mode(status='立项审核失败'))
    db.session.add(Project_mode(status='中期审核失败'))
    db.session.add(Project_mode(status='结题审核失败'))
    db.session.commit()