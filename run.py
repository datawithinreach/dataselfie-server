from flask import Flask, request, Response, jsonify#, render_template
from flask_cors import CORS
import logging
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import sys
# from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
app.config['ENV'] = 'development'

# db authentication
dbauth = next(csv.reader(open('./dbauth.txt', 'r')))
dbauth[0] = dbauth[0].strip()
dbauth[1] = dbauth[1].strip()

dburl = 'mongodb://'+dbauth[0]+':'+dbauth[1]+'@localhost:27017/?authSource=admin'

client  = MongoClient(dburl)
db      = client.dataportraits

@app.route('/login', methods=['POST'])
def login():
	auth = request.get_json()
	user = db.users.find_one({'username': auth['username']})
	# try reading a user 
	if user is not None and check_password_hash(user['password'], auth['password']):
		return jsonify(status=True, message='login successful')
	return jsonify(status=False, message='login failed')

@app.route('/signup', methods=['POST'])
def signup():
	auth = request.get_json()
	user = db.users.find_one({'username': auth['username']})
	# try reading a user 
	if user is not None :
		return jsonify(status=False, message='username is already taken!')
	try:
		auth['password'] = generate_password_hash(auth['password']) # hashing
		db.users.insert_one(auth)
		return jsonify(status=True, message='signup successful')
	except:
		return jsonify(status=False, message='signup failed')
		
if __name__ == '__main__':
	# socketio.run(app, port=app.config['PORT'], host='0.0.0.0', debug=True)
	app.run(port=8889, debug=True)