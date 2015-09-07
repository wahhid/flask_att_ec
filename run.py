# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from flask.json import jsonify

# configuration (could also be in external file...see below)
DATABASE = 'test.db'
DEBUG = True
SECRET_KEY = 'secretkey'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)

# get configuration details (either from this or external file)
app.config.from_object(__name__)

# Set this environment variable using export FLASKR_SETTINGS=....
#FLASKR_SETTINGS = '/Users/mike/SkyDrive/Personal/Education/flask/flaskr/FLASKR_SETTINGS.ini'
#app.config.from_envvar('FLASKR_SETTINGS', silent=False)

# connection to sqlite database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return "<center>Attendance Embedded System</center>"


def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/createemployee', methods=['GET'])
def create_employee():
    try:
        nik = request.args.get('nik')
        name = request.args.get('name')
        g.db.execute('insert into employees (nik, name) values (?, ?)', [nik, name])
        g.db.commit()    
        return jsonify(success=True, message='', result=[])
    except sqlite3.Error, e:
        return jsonify(success=False, message=e.args[0], result=[])
        



@app.route('/allemployee', methods=['GET'])
def all_employee():
    try:
        cur = g.db.execute('select id, nik, name from employees')
        employees = [dict(id=row[0], nik=row[1], name=row[2]) for row in cur.fetchall()]
        return jsonify(success=True, message='', result=employees)
    except sqlite3.Error, e:
        return jsonify(success=False, message=e.args[0], result=[])

if __name__ == '__main__':
    app.run()