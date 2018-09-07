from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import csv
from pymongo import MongoClient

# db authentication
dbauth = next(csv.reader(open('app/database/db_auth.txt', 'r')))
dbauth[0] = dbauth[0].strip()
dbauth[1] = dbauth[1].strip()
dburl = 'mongodb://'+dbauth[0]+':'+dbauth[1]+'@localhost:27017/?authSource=admin'
db = MongoClient(dburl)
db = db.dataselfie
env = Environment(
	loader=PackageLoader('app', 'templates'),
	autoescape=select_autoescape(['html'])
)

url = 'https://dataportrait.namwkim.org'
# Reminder Emails
from app.auth.email import send_email
from apscheduler.schedulers.background import BackgroundScheduler
import app
def reminder():
	# # search for reminders
	forms = list(db.forms.find({'reminder':{'$exists':True}}))

	# email template
	template = env.get_template('reminder.html')
	
	# date 
	today = datetime.utcnow()
	days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	for form in forms:

		# check the reminder schedule
		repeatCycle  = form['reminder']['repeatCycle']
		repeatOption  = form['reminder']['repeatOption']
		if repeatCycle=='daily' or \
			(repeatCycle=='weekly' and repeatOption==days[today.weekday()] ) or\
			(repeatCycle=='monthly' and repeatOption.split(' ')[-1]==today.day) or\
			(repeatCycle=='monthly' and today.day<=7 and repeatOption.split(' ')[-1]==days[today.weekday()]):
			
			# find the owner
			user = db.users.find_one({'username': form['username']})
			if (user is None):
				continue
			subscribers = [user['email']] + form['subscribers']
			
			subject = "Reminder: " + form['title']

			html = template.render(form_url=(url+'/forms/view/'+form['id']))
			
			for to in subscribers:
				print(html, subscribers)
				send_email(to, subject, html)


def run_scheduler():
	scheduler = BackgroundScheduler()
	scheduler.add_job(reminder, 'interval', days=1)
	scheduler.start()

