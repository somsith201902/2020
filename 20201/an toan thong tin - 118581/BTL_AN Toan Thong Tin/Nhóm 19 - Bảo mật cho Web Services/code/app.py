import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
from flask_restful import Api
from flask.views import MethodView
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user

# import predefined variables from setup database file
from database_setup import User, Book, db, app


# REST API
# Method      URI                                    Action
# GET       http://localhost:5000/books/          Retrieve list of books
# GET       http://localhost:5000/books/<bid>     Retrieve a book
# POST      http://localhost:5000/books/          Create a new book

app.secret_key = 'lajsodf08z0.3lk,12jo0z9c21'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
db.init_app(app)
api = Api(app)
login = LoginManager(app)
login.init_app(app)
db.create_all()


@login.user_loader
def load_user(uid):
	return User.query.get(int(uid))

class LoginAPI(MethodView):
	def get(self):
		return make_response(render_template('login.html'))
	def post(self):
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username = username).first()
		if user is None or not user.check_password(password):
			flash('Invalid username or password')
			return make_response(render_template('login.html'))
		login_user(user)
		flash('Log in successfully')
		return make_response(render_template('index.html'))

class LogoutAPI(MethodView):
	def get(self):
		logout_user()
		flash('Log out successfully')
		return make_response(render_template('blank.html'))

class RegisterAPI(MethodView):
	def get(self):
		return make_response(render_template('register.html'))
	def post(self):
		new_username = request.form['username']
		new_password = request.form['password']
		user = User.query.filter_by(username = new_username).first()
		if user is None:
			new_password_hash = generate_password_hash(new_password)
			new_user = User(username = new_username, password_hash = new_password_hash)
			db.session.add(new_user)
			db.session.commit()
			flash('Register successfully')
			return make_response(render_template('blank.html'))
		flash('This username is already existed')
		return make_response(render_template('register.html'))
			
class IndexAPI(MethodView):
	def get(self):
		if current_user.is_authenticated:
			return make_response(render_template('index.html'))
		else:
			return make_response(render_template('blank.html'))

class BookAPI(MethodView):
	decorators = [login_required]
	# retrieve a book information from database
	def get(self, bid):
		result = Book.query.filter_by(bid = bid)
		if result.count():
			result = result.first()
			return make_response(render_template('book.html', result = result))
		else:
			flash('There is no book with BID = {:d}'.format(bid))
			return make_response(render_template('index.html'))

class BookListAPI(MethodView):
	decorators = [login_required]
	# retrieve list of all books
	def get(self):
		result = Book.query.all()
		return make_response(render_template('booklist.html', result = result))
	# insert a new book into database
	def post(self):
		new_title = request.form['title']
		new_author = request.form['author']
		new_genre = request.form['genre']
		new_record = Book(title = new_title, author = new_author, genre = new_genre)
		db.session.add(new_record)
		db.session.commit()
		return make_response(render_template('book.html', result = new_record))


api.add_resource(BookAPI, '/books/<int:bid>/')
api.add_resource(BookListAPI, '/books/')
api.add_resource(IndexAPI, '/')
api.add_resource(LoginAPI, '/login')
api.add_resource(RegisterAPI, '/register')
api.add_resource(LogoutAPI, '/logout')



if __name__ == '__main__':
	app.run(debug = True)

