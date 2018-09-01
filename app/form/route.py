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
	forms = list(db.forms.find({'username': params['username']}).sort('createdAt'))

	return jsonify(status=True, message='success', data=forms)

@form.route('/upsert_form', methods=['POST'])
def upsert_form():
	db = get_db()
	params = request.get_json()
	params['attrs']['createdAt'] = datetime.utcnow()
	try:
		result = db.forms.update_one({'_id': params['formId']}, {'$set':params['attrs']}, upsert=True)
		if result.upserted_id is not None:
			return jsonify(status=True, message='1 form created.')
		elif result.modified_count is 1:
			return jsonify(status=True, message='1 form updated.')
		else:
			return jsonify(status=False, message='Upsert with id = {0}  failed.'.format(params['formId']))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	
@form.route('/delete_form', methods=['POST'])
def delete_form():
	db = get_db()
	params = request.get_json()
	try:
		result = db.forms.delete_one({'_id': params['formId']})
		return jsonify(status=result.deleted_count==1, message='{0} form deleted.'.format(result.deleted_count))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	
@form.route('/request_form_content', methods=['POST'])
def request_form_content():
	db = get_db()
	params = request.get_json()
	try:
		result = db.forms.find_one({'_id':params['formId']})
		if result is None:
			return jsonify(status=False, message='Could not find the form with ID = {0}.'.format(params['formId']))
		
		# the user is not the author
		if ('public' not in result or result['public'] is False) \
			and params['username'] != result['username']:
			return jsonify(status=False, message='{0} do not have access to {1}.'.format(params['username'], params['formId']))
		
		# find questions 
		questions = list(db.questions.find({'formId':params['formId']}).sort('createdAt'))

		# find all options
		options = []
		for question in questions:				
			options += list(db.options.find({'questionId':question['id']}).sort('createdAt'))

		# find all drawings
		drawings = list(db.drawings.find({'parentId':params['formId']}).sort('createdAt'))
		for option in options:
			drawings += list(db.drawings.find({'parentId':option['id']}).sort('createdAt'))

		# find all responses
		responses = list(db.responses.find({'formId':params['formId']}).sort('createdAt'))
	
		data = {'form':result, 'questions':questions, 'options':options, \
			'drawings':drawings, 'responses':responses}
		return jsonify(status=True, message='Successfully fetched the form content.', data=data)
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))


## ---------- question ------------ ##
@form.route('/upsert_question', methods=['POST'])
def upsert_question():
	db = get_db()
	params = request.get_json()
	params['attrs']['createdAt'] = datetime.utcnow()
	try:
		result = db.questions.update_one({'_id': params['questionId']}, {'$set':params['attrs']}, upsert=True)
		if result.upserted_id is not None:
			return jsonify(status=True, message='1 question created.')
		elif result.modified_count is 1:
			return jsonify(status=True, message='1 question updated.')
		else:
			return jsonify(status=False, message='Upsert with id = {0}  failed.'.format(params['questionId']))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	
@form.route('/delete_question', methods=['POST'])
def delete_question():
	db = get_db()
	params = request.get_json()
	try:
		result = db.questions.delete_one({'_id': params['questionId']})
		return jsonify(status=result.deleted_count==1, message='{0} question deleted.'.format(result.deleted_count))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))

## ---------- option ------------ ##
@form.route('/upsert_option', methods=['POST'])
def upsert_option():
	db = get_db()
	params = request.get_json()
	params['attrs']['createdAt'] = datetime.utcnow()
	try:
		result = db.options.update_one({'_id': params['optionId']}, {'$set':params['attrs']}, upsert=True)
		print(result.raw_result)
		if result.upserted_id is not None:
			return jsonify(status=True, message='1 option created.')
		elif result.modified_count is 1:
			return jsonify(status=True, message='1 option updated.')
		else:
			return jsonify(status=False, message='Upsert with id = {0}  failed.'.format(params['optionId']))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	
@form.route('/delete_option', methods=['POST'])
def delete_option():
	db = get_db()
	params = request.get_json()
	try:
		result = db.options.delete_one({'_id': params['optionId']})
		return jsonify(status=result.deleted_count==1, message='{0} option deleted.'.format(result.deleted_count))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))

## ---------- drawing ------------ ##
@form.route('/upsert_drawing', methods=['POST'])
def upsert_drawing():
	db = get_db()
	params = request.get_json()
	params['attrs']['createdAt'] = datetime.utcnow()
	try:
		result = db.drawings.update_one({'_id': params['drawingId']}, {'$set':params['attrs']}, upsert=True)
		if result.upserted_id is not None:
			return jsonify(status=True, message='1 drawing created.')
		elif result.modified_count is 1:
			return jsonify(status=True, message='1 drawing updated.')
		else:
			return jsonify(status=False, message='Upsert with id = {0}  failed.'.format(params['drawingId']))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	
@form.route('/delete_drawing', methods=['POST'])
def delete_drawing():
	db = get_db()
	params = request.get_json()
	try:
		result = db.drawings.delete_one({'_id': params['drawingId']})
		return jsonify(status=result.deleted_count==1, message='{0} drawing deleted.'.format(result.deleted_count))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))

## ---------- response ------------ ##
@form.route('/upsert_response', methods=['POST'])
def upsert_response():
	db = get_db()
	params = request.get_json()
	params['attrs']['createdAt'] = datetime.utcnow()
	try:
		result = db.responses.update_one({'_id': params['responseId']}, {'$set':params['attrs']}, upsert=True)
		if result.upserted_id is not None:
			return jsonify(status=True, message='1 response created.')
		elif result.modified_count is 1:
			return jsonify(status=True, message='1 response updated.')
		else:
			return jsonify(status=False, message='Upsert with id = {0}  failed.'.format(params['responseId']))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))
	
@form.route('/delete_response', methods=['POST'])
def delete_response():
	db = get_db()
	params = request.get_json()
	try:
		result = db.responses.delete_one({'_id': params['responseId']})
		return jsonify(status=result.deleted_count==1, message='{0} response deleted.'.format(result.deleted_count))
	except PyMongoError as e:
		return jsonify(status=False, message=str(e))