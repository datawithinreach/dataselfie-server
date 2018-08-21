import datetime
from flask import Blueprint, request, jsonify, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.email import send_email
from app.auth.token import generate_confirmation_token, confirm_token
from app.database.db import get_db
from string import Template
# auth = Blueprint('auth', __name__)
auth = Blueprint('auth', __name__)

# REST API
@auth.route('/login', methods=['GET','POST'])
def login():
	db = get_db()
	auth = request.get_json()
	user = db.users.find_one({'username': auth['username']})
	if user['confirmed'] is False:
		return jsonify(status=False, message='You have not activated your account yet.')
	# try reading a user 
	if user is not None and check_password_hash(user['password'], auth['password']) is False:
		return jsonify(status=False, message='login failed')
	return jsonify(status=True, message='login successful')
	

@auth.route('/signup', methods=['GET','POST'])
def signup():
	db = get_db()
	auth = request.get_json()
	user = db.users.find_one({'username': auth['username']})
	# try reading a user 
	if user is not None :
		return jsonify(status=False, message='username is already taken!')
	# check email
	email = db.users.find_one({'email': auth['email']})
	if email is not None :
		return jsonify(status=False, message='email is already taken!')
	try:
		auth['password'] = generate_password_hash(auth['password']) # hashing
		auth['confirmed'] = False
		
		db.users.insert_one(auth)
		token = generate_confirmation_token(auth['email'])
		
		confirm_url = url_for('.confirm_email', token=token, _external=True)
		html = render_template('activate.html', confirm_url=confirm_url, username=auth['username'])
		subject = "Please Activate Your DataPortraits Account"
		send_email(auth['email'], subject, html)
		return jsonify(status=True, message='We sent a confirmation email. Please check your email.')
	except:
		return jsonify(status=False, message='signup failed')


@auth.route('/confirm/<token>')
def confirm_email(token):
	db = get_db()
	try:
		email = confirm_token(token)
	except:
		return render_template('confirm.html', message='The confirmation link is invalid or has expired.', success=False) 
	user = db.users.find_one({'email': email})
	if user['confirmed']:
		return render_template('confirm.html', message='Account already confirmed.', success=True) 
	
	user['confirmed'] = True
	db.users.update_one({'email': email}, {'$set':{'confirmed':True, 'confirmed_on': datetime.datetime.now()}} )
	return render_template('confirm.html', message='You have confirmed your account. Thanks!', success=True) 
	

@auth.route('/resend', methods=['GET','POST'])
def resend_confirmation():
	db = get_db()
	auth = request.get_json()
	user = db.users.find_one({'username': auth['username']})
	token = generate_confirmation_token(user['email'])
	confirm_url = url_for('.confirm_email', token=token, _external=True)
	html = render_template('activate.html', confirm_url=confirm_url, username=user['username'])
	subject = "Please Activate Your DataPortraits Account"
	send_email(user['email'], subject, html)
	return jsonify(status=True, message='We sent a new confirmation email. Please check your email.')