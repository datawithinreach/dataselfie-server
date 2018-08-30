import datetime
from flask import Blueprint, request, jsonify, url_for, render_template
from app.database.db import get_db
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

form = Blueprint('form', __name__)

# REST API
@form.route('/request_forms', methods=['POST'])
def request_forms():
	db = get_db()
	params = request.get_json()
	forms = list(db.forms.find({'username': params['username']}))

	return jsonify(status=True, message='success', forms=forms)

@form.route('/upsert_form', methods=['POST'])
def upsert_form():
	db = get_db()
	params = request.get_json()
	try:
		result = db.forms.update_one({'_id': ObjectId(params['formId'])}, {'$set':params}, {'upsert':True})
		return jsonify(status=result.matched_count==1, message='{0} form updated'.format(result.matched_count))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	
@form.route('/delete_form', methods=['POST'])
def delete_form():
	db = get_db()
	params = request.get_json()
	try:
		result = db.forms.delete_one({'_id': ObjectId(params['formId'])})
		return jsonify(status=result.deleted_count==1, message='{0} form deleted'.format(result.deleted_count))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	