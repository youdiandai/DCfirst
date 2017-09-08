#-*- encoding:utf-8 -*-
from flask import render_template,session,redirect,url_for,make_response,send_file,request
from . import main
from .forms import ProjectMid,ProjectEnd
from .. import db
from ..models import User,Collage,Major,User_mode,Project,Funds,ResultsType,Patent,Paper,Report,BusinessPlan,Website,Other,Project_mode,User_Project

