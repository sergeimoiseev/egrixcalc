# -*- coding: utf-8 -*-
# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

question_0 = u"Реши задачу:\n2+2="

q_list = []
with open('quests.txt','rb') as q_file:
    # 'quests.txt'
    fullstr = q_file.read().decode('utf-8')
q_list = fullstr.split('###')
# q_list = [
#             u"Паровоз идет прямо. Куда идет паровоз?",
#             u"Паровоз идет влево. Куда идет паровоз?",
#             u"Паровоз идет назад. Куда идет паровоз?",
#             u"Паровоз идет вправо. Куда идет паровоз?",
#             ]
q_iter = iter(q_list)
current_quest = ""
# configuration
DATABASE = 'app.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'valera'
PASSWORD = 'valera'

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

from contextlib import closing
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# sql3 requests decorators
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    global current_quest, q_iter
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [current_quest, request.form['text']])
                 # [request.form['title']+"\n2+2=", request.form['text']+"\n4"])
    g.db.commit()
    try:
        current_quest = next(q_iter)
    except:
        flash(u"Тест завершен. Для повторного прохождения войди заново.")
        q_iter = iter(q_list)
        return redirect(url_for('login'))
        
    flash(current_quest)
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            global current_quest, q_iter
            current_quest = next(q_iter)
            flash(current_quest)
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()