from  datetime import datetime
from flask import Blueprint, request, jsonify, url_for, render_template
from app.database.db import get_db
# from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

form = Blueprint('form', __name__)

# REST API
@form.route('/request_forms', methods=['POST'])
def request_forms():
	db = get_db()
	params = request.get_json()
	forms = list(db.forms.find({'username': params['username']}))

	return jsonify(status=True, message='success', data=forms)

@form.route('/upsert_form', methods=['POST'])
def upsert_form():
	db = get_db()
	params = request.get_json()
	parems['createdAt'] = datetime.now().timestamp()
	try:
		result = db.forms.update_one({'_id': params['formId']}, {'$set':params['attrs']}, upsert=True)
		if result.upserted_id is not None:
			return jsonify(status=True, message='1 form created')
		elif result.modified_count is 1:
			return jsonify(status=True, message='1 form updated')
		else:
			return jsonify(status=False, message='Upsert with id = {0}  failed'.format(params['formId']))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	
@form.route('/delete_form', methods=['POST'])
def delete_form():
	db = get_db()
	params = request.get_json()
	try:
		result = db.forms.delete_one({'_id': params['formId']})
		return jsonify(status=result.deleted_count==1, message='{0} form deleted'.format(result.deleted_count))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	
@form.route('/request_form_content', methods=['POST'])
def request_form_content():
	db = get_db()
	params = request.get_json()
	print(params)
	try:
		result = db.forms.find_one({'_id':params['formId']})
		if result is None:
			return jsonify(status=False, message='Could not find the form with ID = {0}'.format(params['formId']))
		
		if ('public' not in result or result['public'] is False) \
			and params['username'] != result['username']:
			return jsonify(status=False, message='{0} do not have access to {1}'.format(params['username'], params['formId']))
		
		if params['username'] == result['username']:
			# find questions 
			questions = list(db.questions.find({'formId':params['formId']}))

			# find options
			options = []
			for question in questions:				
				options += list(db.options.find({'questionId':question['id']}))

			# find drawings
			drawings = list(db.drawings.find({'formId':params['formId']}))
			for option in options:
				drawings += list(db.drawings.find({'optionId':option['id']}))

			# find responses
			responses = list(db.responses.find({'formId':params['formId']}))
		else: # the user is not the author
			# is not public
			if 'public' not in result or result['public'] is False:
				return jsonify(status=False, message='{0} do not have access to {1}'.format(params['username'], params['formId']))
	
		return jsonify(status=result.deleted_count==1, message='{0} form deleted'.format(result.deleted_count))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
