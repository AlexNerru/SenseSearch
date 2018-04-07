import sqlite3
import User
import os

conn_str = 'sense_search'

class DataBaseServise():

	def getAllUsers(self):
		os.chmod('C:\\Users\\AlexNerru\\PycharmProjects\\HackTheMedia', 0o644)
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
		os.chmod('C:\\Users\\AlexNerru\\PycharmProjects\\HackTheMedia', 0o644)
		conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),
					      conn_str))
		cur = conn.cursor()
		cur.execute('INSERT INTO users (login, password)VALUES (?,?)', (user._login,user._password))
		print(cur.fetchall())
		conn.commit()
		conn.close()