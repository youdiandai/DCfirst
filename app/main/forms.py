#-*- encoding:utf-8 -*-
from wtforms.validators import DataRequired,equal_to,Email
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,RadioField,TextAreaField,SelectField,FileField


#中期申报表单
class ProjectMid(Form):
    MidProgress = TextAreaField("研究工作进展情况")
    file = FileField("提交成果物")
    submit = SubmitField('提交')

#结题报告表单
class ProjectEnd(Form):
    ResultsDescribe = TextAreaField("项目成果简介")
    ResultsSummary = TextAreaField("项目总结报告")
    Problems = TextAreaField("项目遇到的问题和建议")
    file = FileField("提交成果物")
    submit = SubmitField('提交')
