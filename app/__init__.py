import os, csv
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail




app = Flask(__name__)
app.config.from_object('config')

# app.config['DEBUG'] = 'development'
# app.config['PORT'] = 8889

# app.config['ENV'] = 'development'
# app.config['SECRET_KEY'] = 'dataportraits'
# app.config['SECURITY_PASSWORD_SALT'] = 'dataportraits_salt_peppers'

# app.config['MAIL_SERVER '] = 'smtp.googlemail.com'
# app.config['MAIL_PORT '] = '465'
# app.config['MAIL_USE_TLS '] = False
# app.config['MAIL_USE_SSL '] = True

# email_auth = next(csv.reader(open('./email_auth.txt', 'r')))
# email_auth[0] = email_auth[0].strip()
# email_auth[1] = email_auth[1].strip()

# app.config['MAIL_USERNAME'] = email_auth[0]
# app.config['MAIL_PASSWORD'] = email_auth[1]
# app.config['MAIL_DEFAULT_SENDER'] = 'namwkim85@gmail.com'
# decorate
CORS(app)
mail = Mail(app)

# import blueprints here otherwise, circular imports will attempt to access mail which is not defined yet
from app.auth.route import auth
from app.form.route import form
from app.database.db import close_db
# blurprints
app.register_blueprint(auth)
app.register_blueprint(form)

app.teardown_appcontext(close_db)