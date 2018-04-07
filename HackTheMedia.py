from flask import Flask, render_template
import flask
import flask_login
from DataBaseService import DataBaseServise
from User import User

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'sense search forever'
users = {}


@app.route('/')
def main():

	db = DataBaseServise()
	print(db.getAllUsers())
	global users
	users = db.getAllUsers()
	return render_template('index.html')


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


@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

	email = flask.request.form['email']
	try:
		if flask.request.form['password'] == users[email]:
			user = User()
			user.id = email
			flask_login.login_user(user)
			return flask.redirect(flask.url_for('protected'))
	except (KeyError):
		return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
	return 'Logged in as: ' + flask_login.current_user.id


@login_manager.unauthorized_handler
def unauthorized_handler():
	return 'Unauthorized'


if __name__ == '__main__':
	app.run()
