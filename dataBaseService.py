import sqlite3
from film import Film, Tag
import user
from emotion import emotion
import os

conn_str = 'sense_search'

def comp(args):
	return args.percent


class DataBaseServise():

	def getAllUsers(self):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
					      conn_str))
		cur = conn.cursor()
		cur.execute('SELECT * FROM users')
		users = cur.fetchall()
		dict = {}
		for user in users:
			dict[user[1]] = user[2]
		conn.commit()
		conn.close()
		return dict

	def addUserFilm(self, user_id, film_id):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('INSERT INTO user_films (user_id, film_id)VALUES (?,?)', (user_id, film_id))
		conn.commit()
		conn.close()


	def addUser(self, user):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
					      conn_str))
		cur = conn.cursor()
		cur.execute('INSERT INTO users (login, password)VALUES (?,?)', (user._login,user._password))
		conn.commit()
		conn.close()


	def addFilm(self, film):
		print("in func")
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		default_url = 'static/imgs/улица.jpg'
		cur.execute('INSERT INTO films (name,img_url)VALUES (?,?)', (film._name,default_url,))
		cur.execute('SELECT id FROM films WHERE name=?', (film._name,))
		film_id = cur.fetchone()
		print (film_id)
		cur.execute('INSERT INTO emotions VALUES (?,?,?,?,?,?,?,?)', (film_id[0],0,0,0,0,0,0,0))
		conn.commit()
		conn.close()

	def getAllUserFilmsIds(self, user_id):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('SELECT * FROM user_films WHERE user_id = ?', (user_id[0],))
		films = cur.fetchall()
		film_ids = []
		for film in films:
			film_ids.append(film[1])
		conn.commit()
		conn.close()
		return film_ids

	def getFilmById(self, film_id):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()

		cur.execute('SELECT * FROM films WHERE id=?', (film_id,))
		film = cur.fetchone()
		cur.execute('SELECT * FROM emotions WHERE id=?', (film_id,))
		emotion = cur.fetchone()
		emotags = [Tag('angry', emotion[1]), Tag('disgust', emotion[2]), Tag('fear', emotion[3]), Tag('happy',
																										  emotion[4])
		, Tag('neutral', emotion[5]), Tag('sad', emotion[6]), Tag('surprise', emotion[7])]
		film_obj = Film(film[1])

		emotags = sorted(emotags, key=comp)[-3:]
		film_obj.img_url = film[2]
		film_obj.emotags = emotags
		return film_obj

	def getFilmsEmotions(self, film_id):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('SELECT * FROM emotions WHERE id = ?', (film_id,))
		emotion = cur.fetchone()
		conn.commit()
		conn.close()
		return emotion


	def getAllFilms(self):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('SELECT * FROM films')
		all = cur.fetchall()
		films = []
		for film in all:
			cur.execute('SELECT * FROM emotions WHERE id=?',(film[0],))
			emotion = cur.fetchone()
			emotags=[Tag('angry', emotion[1]), Tag('disgust',emotion[2]), Tag('fear', emotion[3]), Tag('happy',
																									   emotion[4])
					 ,Tag('neutral', emotion[5]), Tag('sad',emotion[6]),Tag('surprise',emotion[7])]
			film_obj = Film(film[1])

			emotags = sorted(emotags, key=comp)[-3:]
			film_obj.img_url = film[2]
			film_obj.emotags = emotags
			films.append(film_obj)
		return films


	def updateFilmEmotions(self, id, angry, disgust,fear, happy, neutral, sad,surprise):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('UPDATE emotions SET angry=?, disgust=?, fear=?, happy=?, neutral=?,sad=?,surprise=? WHERE id=?',
					(angry, disgust,fear, happy, neutral, sad,surprise,id[0],))

		conn.commit()
		conn.close()


	def getFilmIdByName(self,name):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('SELECT id FROM films WHERE name = ?', (name,))
		film_id = cur.fetchone()
		conn.commit()
		conn.close()
		return film_id

	def getUserIdByName(self, name):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('SELECT id FROM users WHERE login = ?', (name,))
		user_id = cur.fetchone()
		conn.commit()
		conn.close()
		return user_id
	
	def getFilm(self, name):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('SELECT * FROM films')
		all = cur.fetchall()
		for film in all:
			if (film[1] == name):
				cur.execute('SELECT * FROM emotions WHERE id=?',(film[0],))
				emotion = cur.fetchone()
				emotags=[Tag('angry', emotion[1]), Tag('disgust',emotion[2]), Tag('fear', emotion[3]), Tag('happy',
																									   emotion[4])
					 ,Tag('neutral', emotion[5]), Tag('sad',emotion[6]),Tag('surprise',emotion[7])]
				film_obj = Film(film[1])
				film_obj.img_url = film[2]
				emotags = []
				for em in sorted(emotags, key=comp)[-3:]:
					if em.percent > 0:
						emotags.append(em)
				film_obj.emotags = emotags
				return film_obj
