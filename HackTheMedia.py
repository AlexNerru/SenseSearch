from flask import Flask, render_template, redirect, url_for, request
import flask
import flask_login
import sqlite3
from DataBaseService import DataBaseServise
from User import User
import os
import uuid
from Film import Film
import emoapi 

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'sense search forever'
users = {}

def AddFromOneDbToAnother ():
	conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
										'films.sqlite'))
	cur = conn.cursor()
	cur.execute('SELECT * FROM import')
	films = cur.fetchall()
	conn.commit()
	conn.close()
	db = DataBaseServise()
	for film in films:
		db.addFilm(Film(film[14]))
		print(db.getFilmIdByName(film[14]))
		print(film[16])
		db.updateFilmEmotions(db.getFilmIdByName(film[14]),film[2],film[5],film[7],film[9],film[11],film[13],film[16])

@app.route('/profile', methods=['GET','POST'])
def profile():
	return render_template('ProfilePage.html', name=request.args.get("name"))

@app.route('/load',methods=['GET', 'POST'])
def load():
	if flask.request.method == 'GET':
		return render_template('Load.html')
	elif flask.request.method == 'POST':
		if 'file' not in flask.request.files:
			flask.flash('No file part')
			return redirect(flask.request.url)
		file = flask.request.files['file']
		file_name = file.filename
		extension = os.path.splitext(file_name)[1]
		finalName = str(uuid.uuid4()) + str(extension)
		file_path_small = os.path.join(os.path.dirname(os.path.realpath(__file__)),
									   'videos')
		file_path = os.path.join(file_path_small, finalName)
		file.save(file_path)
		emotion = emoapi.videoemot(file_path)
		print(emotion)
		return render_template('Load.html')

@app.route('/', methods=['GET', 'POST'])
def main():
	#AddFromOneDbToAnother()
	db = DataBaseServise()
	db.getAllFilms()
	global users
	users = db.getAllUsers()
	print(flask.request.method)
	print(flask.request)
	if flask.request.method == 'GET':
		return render_template('MainPage.html', signed = False, films = db.getAllFilms())
	print(flask.request.form)
	if 'quit' in flask.request.form:
		return render_template('MainPage.html', signed=False)
	if 'email' in flask.request.form:
		email = flask.request.form['email']

		if email in users:
			if flask.request.form['password'] == users[email]:
				user = User()
				user.id = email
				user._login = flask.request.form['email']
				user._password = flask.request.form['password']
				flask_login.login_user(user)
				return render_template('MainPage.html', signed = True,  name = flask.request.form['email'], films = db.getAllFilms())
			else:
				return 'Bad login'
		else:
			return 'No login'
	else:
		user = User()
		user.id = flask.request.form['uname']
		user._login = flask.request.form['uname']
		user._password = flask.request.form['psw']
		try:
			db.addUser(user)
		except (sqlite3.IntegrityError):
			return 'Already exist'
		return render_template('MainPage.html', signed = True, name = flask.request.form['uname'])


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
