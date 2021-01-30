#!/usr/bin/python3

import sqlite3

from flask import *
from flask_login import *
from flask_login import LoginManager
from os.path import exists, dirname
from os import mkdir
from hashed import hashed
from misc import *
from user import User

USERSDB = 'databases/users.db'
QUIZZESDB = 'databases/quizzes.db'
if dirname(USERSDB) and not exists(dirname(USERSDB)):
    mkdir(dirname(USERSDB))
if dirname(QUIZZESDB) and not exists(dirname(QUIZZESDB)):
    mkdir(dirname(QUIZZESDB))

app = Flask(__name__, '/', 'static')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = lambda: User(0, 'anonymous', hashed(''))
login_manager.login_view = '/login'

users_conn = sqlite3.connect(USERSDB)
users_cur = users_conn.cursor()
users_cur.execute('''CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	BLOB NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)''')
users_conn.commit()

if not users_cur.execute('SELECT \'1\' FROM users WHERE username="anonymous"').fetchall():
    # users_cur.execute(
    #    'INSERT INTO users VALUES (0, ?, ?)',
    #    ('anonymous', hashed(''))
    # )
    users_cur.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="users"')
    users_conn.commit()

quizzes_conn = sqlite3.connect(QUIZZESDB)
quizzes_cur = quizzes_conn.cursor()
quizzes_cur.execute('''CREATE TABLE IF NOT EXISTS "quizzes" (
	"id"	INTEGER NOT NULL UNIQUE,
	"questions"	INTEGER NOT NULL,
	"object"	BLOB NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)''')
quizzes_conn.commit()

users_cur.execute('SELECT id, username, password FROM users')
users = {}
users_name = {}
for user in users_cur.fetchall():
    u = User.from_db(user)
    users[str(user[0])] = u
    users_name[str(user[1])] = u
print('# of users:', len(users))


@login_manager.user_loader
def user_loader(id: str):
    return users.get(id, None)


@app.before_request
def before_request():
    print('login', current_user.name)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return alert('You are already loggin in as %s' % current_user.name)
    if request.method.upper() == 'GET':
        return render_template('login.html')
    name = request.values.get('username', ...)
    pwd = request.values.get('password', ...)
    if name is ... or pwd is ...:
        return alert('Please fill in the entire form!')
    u = users_name.get(name, ...)
    if u is ... or u.pwd != hashed(pwd):
        return alert('User not found or password does not match!')
    if not login_user(u):
        return alert('Login failed!')
    return redirect('/')


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect('/')


@app.route('/signup', methods=['POST', 'GET'])
def signup_page():
    if request.method.upper() == 'GET':
        return render_template('signup.html')
    name = request.values.get('username', ...)
    pwd = request.values.get('password', ...)
    pwd2 = request.values.get('password2', ...)
    if name is ... or pwd is ... or pwd2 is ...:
        return alert('Please fill in the entire form!')
    if pwd != pwd2:
        return alert('Passwords do not match!')
    conn = sqlite3.connect(USERSDB)
    cur = conn.cursor()
    if cur.execute('SELECT \'1\' FROM users WHERE username=?', (name,)).fetchall():
        return alert('User already exists, please login', '/login')
    cur.execute(
        'INSERT INTO users(username, password) VALUES (?, ?)',
        (name, hashed(pwd))
    )
    conn.commit()
    id = cur.execute('SELECT id FROM users WHERE username=?', (name,))
    u = User(id, name, pwd)
    users[id] = users_name[name] = u
    return alert('Sign up complete, please login', '/login')


@app.route('/editor')
def editor_page():
    return render_template('editor.html')


if __name__ == '__main__':
    app.secret_key = 'gjtnc kvdbfvh cvjhbdfhnjgkfrhkgvjdkhfyenrtby5tgvutrh ygtvytrguthn'
    app.run('0.0.0.0', 8008, True)
