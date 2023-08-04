from flask import render_template,url_for,redirect,request,Blueprint
from puppycompanyblog.models import User, BlogPost
from puppycompanyblog import db

users = Blueprint('users', __name__)
@users.route('/list')
def listall():
	return render_template('list.html',user= User.query.all())
