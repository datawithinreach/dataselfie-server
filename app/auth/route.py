import datetime
from flask import Blueprint, request, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.email import send_email
from app.auth.token import generate_confirmation_token, confirm_token
from app.database.db import get_db
from string import Template
# auth = Blueprint('auth', __name__)
auth = Blueprint('auth', __name__)

# confirmation string template
confirmHTML = Template('<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p>\
	<p><a href="$confirm_url">$confirm_url</a></p><br><p>Cheers!</p>')
# REST API
@auth.route('/login', methods=['GET','POST'])
def login():
	db = get_db()
	auth = request.get_json()
	user = db.users.find_one({'username': auth['username']})
	# try reading a user 
	if user is not None and check_password_hash(user['password'], auth['password']):
		return jsonify(status=True, message='login successful')
	return jsonify(status=False, message='login failed')

@auth.route('/signup', methods=['GET','POST'])
def signup():
	db = get_db()
	auth = request.get_json()
	user = db.users.find_one({'username': auth['username']})
	# try reading a user 
	if user is not None :
		return jsonify(status=False, message='username is already taken!')
	try:
		auth['password'] = generate_password_hash(auth['password']) # hashing
		auth['confirmed'] = False
		
		db.users.insert_one(auth)
		token = generate_confirmation_token(auth['email'])
		
		confirm_url = url_for('.confirm_email', token=token, _external=True)
		html = confirmHTML.substitute(confirm_url=confirm_url)
		subject = "DataPortraits - Please confirm your email"
		
		send_email(auth['email'], subject, html)
		print('success', auth['email'], send_email)
		return jsonify(status=True, message='We sent a confirmation email. Please check your email.')
	except:
		return jsonify(status=False, message='signup failed')


@auth.route('/confirm/<token>')
def confirm_email(token):
	db = get_db()
	try:
		email = confirm_token(token)
	except:
		return '<p>The confirmation link is invalid or has expired.</p>'
	user = db.users.find_one({'email': email})
	if user['confirmed']:
		return '<p>Account already confirmed. Please login.</p>'
	
	user['confirmed'] = True
	db.users.update_one({'email': email}, {'$set':{'confirmed':True, 'confirmed_on': datetime.datetime.now()}} )

	return '<p>You have confirmed your account. Thanks!</p>'