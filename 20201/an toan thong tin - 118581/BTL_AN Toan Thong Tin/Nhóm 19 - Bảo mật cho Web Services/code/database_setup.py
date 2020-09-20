from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# set up a database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookdb.db'
app.config['SQLALCHEMY_BINDS'] = {
	'users' : 'sqlite:///userdb.db'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
	__tablename__ = 'Books'
	bid = db.Column(db.Integer(), primary_key = True)
	title = db.Column(db.String(256))
	author = db.Column(db.String(256))
	genre = db.Column(db.String(256))

	def get_id(self):
		return self.bid


class User(UserMixin, db.Model):
	__tablename__ = 'Users'
	__bind_key__ = 'users'
	uid = db.Column(db.Integer(), primary_key = True)
	username = db.Column(db.String(256))
	password_hash = db.Column(db.String(256))

	def get_id(self):
		return self.uid

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


