import sqlite3
import os
import time
from flask import Flask, render_template, session, g, request, redirect, url_for, flash

# import my own module
from forms import ContactForm

DATABASE= '/home/alstr/Downloads/NEW-bloggprojekt-master/blogdatabase.db'
USERNAME='Karlshamn'
PASSWORD='webteknologi'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'medieteknik'

#  Connects to the specific database
def connect_db():
    db = sqlite3.connect('DATABASE')
    db.row_factory = sqlite3.Row
    return db

#  Initialize the database
def init_db():
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb():
    init_db()
    print ('Initialized the database.')

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        return g.sqlite_db

#  Close database connection
@app.teardown_appcontext
def close_connection(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.cli.command('addtable')
def create_table():
    db = connect_db()
    curs = db.execute('CREATE TABLE IF NOT EXISTS thread(user TEXT, comment TEXT, created DATETIME)')
    print ('Added the new table successfully!')

@app.cli.command('addusertable')
def create_table():
    db = connect_db()
    curs = db.execute('CREATE TABLE IF NOT EXISTS user(name TEXT, email TEXT)')
    print ('Added the new table successfully!')

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/blog')
def blog():
    db = connect_db()
    curs = db.execute('SELECT title, post, author FROM posts')
    posts = curs.fetchall()
    return render_template("blogposts.html", posts=posts)

#  Login to add post
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid password or username!')
    return render_template('login.html')

# Logout and go back to homepage
@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You were logged out')
    return redirect(url_for('homepage'))

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/admin/list')
def admin_contact():
    db = connect_db()
    curs = db.execute('SELECT name, email FROM user')
    users = curs.fetchall()
    return render_template("list_users.html", users=users)

@app.route('/form')
def add_blog():
    return render_template("form.html")

# add title and text
@app.route('/form/save', methods=['POST'])
def add_posts():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('INSERT INTO posts (title, post, author) VALUES (?, ?, ?)', [request.form['title'], request.form['post'], request.form['author']])
    db.commit()
    return redirect(url_for('add_blog'))

@app.route('/contact', methods=('GET', 'POST'))
def addContact():
    form = ContactForm(csrf_enabled=True)

    if  request.method == "POST":
        db = get_db()
        db.execute('INSERT INTO user (name, email) VALUES (?,?)', (form.name.data, form.email.data))
        db.commit()
        return redirect(url_for('homepage'))
    else:
        return render_template('contact.html', form=form)

if __name__ == "__main__":
    app.run()
