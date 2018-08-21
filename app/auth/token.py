# project/token.py

from itsdangerous import URLSafeTimedSerializer

from flask import current_app as app


def generate_confirmation_token(email):
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600*24*3): # 3 days
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	try:
		email = serializer.loads(
			token,
			salt=app.config['SECURITY_PASSWORD_SALT'],
			max_age=expiration
		)
	except:
		return False
	return email