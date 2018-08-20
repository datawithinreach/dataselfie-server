from flask import g
import csv
from pymongo import MongoClient
# db authentication
dbauth = next(csv.reader(open('app/database/db_auth.txt', 'r')))
dbauth[0] = dbauth[0].strip()
dbauth[1] = dbauth[1].strip()

dburl = 'mongodb://'+dbauth[0]+':'+dbauth[1]+'@localhost:27017/?authSource=admin'


def get_db():
	if 'db' not in g:
		g.db = MongoClient(dburl)
	return g.db.dataportraits


def close_db(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()

