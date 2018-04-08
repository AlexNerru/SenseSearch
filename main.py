from flask import Flask, render_template, redirect, url_for, request, make_response
import flask
import flask_login
import sqlite3
from dataBaseService import DataBaseServise
from user import User
import os
import uuid
from operator import itemgetter
from film import Film
import emoapi
import helper
import tensorflow as tf
from film import Tag

graph = tf.get_default_graph()

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'sense search forever'
users = {}


def AddFromOneDbToAnother():
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
		db.updateFilmEmotions(db.getFilmIdByName(film[14]), film[2], film[5], film[7], film[9], film[11], film[13],
							  film[16])



@app.route('/search', methods=['Post'])
def search():
	tags = flask.request.form['tags']
	array_tags = tags.split(';')
	res_tags = []
	for tag in array_tags:
		if tag.strip() != '':
			res_tags.append(tag.strip())
	db = DataBaseServise()
	films = db.getAllFilms()
	array_of_correct_films = []
	for film in films:
		has = False
		for tag in film.emotags:
			if tag.name in res_tags:
				has = True
				break
		if has:
			array_of_correct_films.append(film)
	return render_template('MainPage.html', signed=request.args.get('signed'), films=array_of_correct_films,
						   name = request.args.get('name'))

def comp(args):
	return args.percent


def getHigherEmoTags(name, films):
	pop_tags = []
	for film in films:
		for tag in film.emotags:
			name = tag.name
			inc = False
			for i in range(0, len(pop_tags)):
				if pop_tags[i].name == name:
					pop_tags[i].percent += 1
					inc = True
			if not inc:
				pop_tags.append(Tag(name, 1))

	return sorted(pop_tags, key=comp)[-3:]

def getRecommend(pop_tags, all_films):
	films = []

	tag_names = []
	for tag in pop_tags:
		tag_names.append(tag.name)

	for film in all_films:
		counter = 0
		for tag in film.emotags:
			if tag.name in tag_names:
				counter += 1
		if counter >= 2:
			films.append(film)
	return films


@app.route('/profile', methods=['GET', 'POST'])
def profile():
	db = DataBaseServise()
	films = getUserFilmsObj(db.getUserIdByName(request.args.get("name")))
	pop_tags = getHigherEmoTags(request.args.get("name"), films)
	return render_template('ProfilePage.html', name=request.args.get("name"), films=films, pop_tags=pop_tags)


@app.route('/load', methods=['GET', 'POST'])
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
		emotion = None
		global graph
		with graph.as_default():
			try:
				emotion = emoapi.videoemot(file_path)
			except:
				emotion = None
		if emotion:
			ans = []
			for k, v in sorted(emotion.items(), key=itemgetter(1))[-2:]:
				if v > 0:
					ans.append(k)
			if ans:
				print(ans)
				headers = {'Content-Type': 'text/html'}
				return make_response(render_template('Load.html', film=ans), 200, headers)
			else:
				return render_template('Load.html', error="Не выделил эмоции")
		else:
			return render_template('Load.html', error="Не выделил эмоции")

def addFilmsToUsers():
	db = DataBaseServise()
	db.addUserFilm(9,14)
	db.addUserFilm(9, 15)
	db.addUserFilm(9, 23)
	db.addUserFilm(10, 14)
	db.addUserFilm(10, 15)
	db.addUserFilm(10, 23)
	db.addUserFilm(11, 15)
	db.addUserFilm(11, 17)
	db.addUserFilm(11, 18)

def getUserFilmsObj (user_id):
	db = DataBaseServise()
	# addFilmsToUsers()
	ids = db.getAllUserFilmsIds(user_id)
	for i in ids:
		print(i)
	films = []
	for id in ids:
		print (id)
		films.append(db.getFilmById(id))
	return films


@app.route('/', methods=['GET', 'POST'])
def main():
	# AddFromOneDbToAnother()
	db = DataBaseServise()
	#addFilmsToUsers()
	#db.addFilm(Film('остров 1 сезон 510 серия'))
	#db.updateFilmEmotions(db.getFilmIdByName('остров 1 сезон 510 серия'),12.02491149,0.644115514,2.747088683,
	#					  20.59463379,31.89011645,31.81333447,0.285799599)

	#берет все фильмы юзера

	global users
	users = db.getAllUsers()
	if flask.request.method == 'GET':
		return render_template('MainPage.html', signed=False, films=db.getAllFilms())
	print(flask.request.form)
	if 'quit' in flask.request.form:
		return render_template('MainPage.html', signed=False, films=db.getAllFilms())
	if 'email' in flask.request.form:
		email = flask.request.form['email']

		if email in users:
			if flask.request.form['password'] == users[email]:
				user = User()
				user.id = email
				user._login = flask.request.form['email']
				user._password = flask.request.form['password']
				flask_login.login_user(user)

				all_films = db.getAllFilms()

				films_of_user = getUserFilmsObj(db.getUserIdByName(flask.request.form['email']))
				pop_tags = getHigherEmoTags(flask.request.form['email'], films_of_user)

				recommended_films = getRecommend(pop_tags, all_films)
				res_recommended_films = []
				for film in recommended_films:
					flag = True
					for i in range(len(films_of_user)):
						if (film._name == films_of_user[i]._name):
							flag = False
					if flag:
						res_recommended_films.append(film)

				return render_template('MainPage.html', signed=True, name=flask.request.form['email'],
									   films=res_recommended_films)
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
		return render_template('MainPage.html', signed=True, name=flask.request.form['uname'], films=db.getAllFilms())


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
	app.run(threaded=True, debug=True)
