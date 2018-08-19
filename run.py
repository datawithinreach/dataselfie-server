from flask import Flask#, render_template
from pymongo import MongoClient
# from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['PORT'] = 5501


# db authentication
dbauth = csv.reader(open('./dbauth.txt', 'r')).next()
dbauth[0] = dbauth[0].strip()
dbauth[1] = dbauth[1].strip()

dburl = 'mongodb://'+dbauth[0]+':'+dbauth[1]+'@localhost:27017/?authSource=admin'

client  = MongoClient(dburl)
db      = client.dataportraits

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
	# socketio.run(app, port=app.config['PORT'], host='0.0.0.0', debug=True)
	app.run(port=9999, debug=True)