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

		cur.execute('SELECT id FROM users WHERE login=?', (user._login,))
		user_id = cur.fetchone()
		cur.execute('INSERT INTO emotions VALUES (?,?,?,?,?,?,?,?)', (user_id[0],0,0,0,0,0,0,0))
		conn.commit()
		conn.close()

	def getUserEPortrait(self, user_id):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('SELECT * FROM emotions WHERE id = ?', (user_id,))
		emotion = cur.fetchone()
		conn.commit()
		conn.close()
		return emotion

	def updateUserEmotions(self, id, angry, disgust,fear, happy, neutral, sad,surprise):
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
											conn_str))
		cur = conn.cursor()
		cur.execute('UPDATE emotions SET angry=?, disgust=?, fear=?, happy=?, neutral=?,sad=?,surprise=? ',
					(angry, disgust,fear, happy, neutral, sad,surprise))

		conn.commit()
		conn.close()
