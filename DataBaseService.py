import sqlite3
import User
from Emotion import emotion
import os

conn_str = 'sense_search'

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

	def addUser(self, user):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
					      conn_str))
		cur = conn.cursor()
		cur.execute('INSERT INTO users (login, password)VALUES (?,?)', (user._login,user._password))
		conn.commit()
		conn.close()

	def addFilm(self, film):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('INSERT INTO films (name)VALUES (?)', (film._name,))
		cur.execute('SELECT id FROM films WHERE name=?', (film._name,))
		film_id = cur.fetchone()
		cur.execute('INSERT INTO emotions VALUES (?,?,?,?,?,?,?,?)', (film_id[0],0,0,0,0,0,0,0))
		conn.commit()
		conn.close()

	def getFilmsEmotions(self, film_id):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('SELECT * FROM emotions WHERE id = ?', (film_id,))
		emotion = cur.fetchone()
		conn.commit()
		conn.close()
		return emotion

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
