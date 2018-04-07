from flask import Flask, render_template
import flask
import flask_login
import sqlite3
from DataBaseService import DataBaseServise
from User import User

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'sense search forever'
users = {}


@app.route('/', methods=['GET', 'POST'])
def main():
	db = DataBaseServise()
	global users
	users = db.getAllUsers()
	if flask.request.method == 'GET':
		print(users)
		return render_template('MainPage.html')

	print(flask.request.form)
	if 'email' in flask.request.form:
		email = flask.request.form['email']
		if flask.request.form['password'] == users[email]:
			user = User()
			user.id = email
			flask_login.login_user(user)
			return flask.redirect(flask.url_for('protected'))
		else:
			return 'Bad login'
	else:
		user = User()
		user._login = flask.request.form['uname']
		user._password = flask.request.form['psw']
		try:
			db.addUser(user)
		except (sqlite3.IntegrityError):
			return 'Already exist'
		return render_template('MainPage.html')





@login_manager.user_loader
def user_loader(email):
	if email not in users:
		return

	user = User()
	user.id = email
	return user


@login_manager.request_loader
def request_loader(request):
	email = request.form.get('email')
	if email not in users:
		return

	user = User()
	user.id = email
	user.is_authenticated = request.form['password'] == users[email]

	return user


@app.route('/protected')
@flask_login.login_required
def protected():
	return 'Logged in as: ' + flask_login.current_user.id


@login_manager.unauthorized_handler
def unauthorized_handler():
	return 'Unauthorized'


if __name__ == '__main__':
	app.run()
