import os
import logging
import pymysql
from logging.handlers import RotatingFileHandler
import sys
from flask import Flask, url_for, request, render_template, redirect, flash, make_response,session
app = Flask(__name__)



@app.route('/login4', methods=['GET', 'POST']) #using sessions
def login4():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']) and \
        if_flash(request.form['username'], request.form['password']): #if statement with multiple strings
            session['username'] = request.form.get('username')
            if if_flash(request.form['username'], request.form['password']):
                flash("Succesfully logged in")
            else:
                flash('Please enter credentials')
            return redirect(url_for('welcome'))
        else:
            error = 'Incorrect username and password'
            app.logger.warning('Incorrect username and password for user (%s)', request.form.get('username'))
    return render_template('login4.html', error=error)
    
@app.route('/login3', methods=['GET', 'POST']) #using cookies
def login3():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            response = make_response(redirect(url_for('welcome')))
            response.set_cookie('username', request.form.get('username'))
            if if_flash(request.form['username'], request.form['password']):
                flash("Succesfully logged in")
            else:
                flash('Please enter credentials')
            return (response)#, username, password)
        else:
            error = 'Incorrect username and password'
    return render_template('login3.html', error=error)

@app.route('/') #using sessions
def welcome4():
    if 'username' in session:
        return render_template('welcome4.html', username=session['username'])
    else:
        return redirect(url_for('login4'))
    
@app.route('/logout4') #using sessions
def logout4():
    session.pop('username', None)  
    return redirect(url_for('login4'))

@app.route('/logout') #using cookies
def logout():
    response = make_response(redirect(url_for('login3')))
    response.set_cookie('username', '', expires=0)
    return response

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            #flash("Succesfully logged in")
            return redirect(url_for('welcome', username=request.form.get('username')))
        else:
            error = 'Incorrect username and password'
    return render_template('login.html', error=error)
    
def valid_login(username, password): #helper function without route
    #mysql block
    MYSQL_DATABASE_HOST = os.getenv('IP', '0.0.0.0')
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'a6771330'
    MYSQL_DATABASE_DB = 'my_flask_app'
    conn = pymysql.connect(
        host = MYSQL_DATABASE_HOST,
        user = MYSQL_DATABASE_USER,
        passwd = MYSQL_DATABASE_PASSWORD,
        db = MYSQL_DATABASE_DB
        )
    cursor = conn.cursor()
    cursor.execute('SELECT * from user WHERE username="%s" AND password="%s"' % (username, password))
    data = cursor.fetchone()
    if data:
        return True
    else:
        return False
        
def if_flash(username, password):
    if username and password:
        return True
    else:
        return False

@app.route('/')
def welcome():
    username = request.cookies.get('username')
    if username:
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('login3'))
        
@app.route('/hellow')
@app.route('/hellow/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/login1', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        return 'username is ' + request.values['username']
    else:
        return '<form method="post" action="/login1"><input type="text" name="username" /><p><button type="submit">Submit</button></form>'

@app.route('/login', methods=['GET'])
def login():
    if request.values:
        return 'username is ' + request.values['username']
    else:
        return '<form method="get" action="/login"><input type="text" name="username" /><p><button type="submit">Submit</button></form>'

@app.route('/')
def index():
    
    return 'index page. powered by Python v' + ".".join([str(x) for x in sys.version_info[0:3]]) + ', ' + sys.version_info[3]

@app.route('/url_for')
def url_for_demo():
    return url_for('show_user_profile', username='richard')
    
@app.route('/user/<username>')
def show_user_profile(username):
    return 'User {}'.format(username)
    
@app.route('/hello')
def hello_world():
    #import pdb; pdb.set_trace() #from cli press 'n' to next or can execute commands, f.e. print(i)
    i = 1
    return 'You visited ' + str(i) + ' times'

@app.route('/post/<int:post_id>') #define that post_id must be integer
def show_post(post_id):
    return 'Post {}'.format(post_id)
    
if __name__ == '__main__':
    host = '0.0.0.0'
    port = 55000
    app.debug = True
    #app.secret_key = 'simple_super_secret_key' #for flashing messages
    app.secret_key = '\xf5\x99*\xd7\x9e:U\xcf2`\t-\xa9\x90"\xe2\xc1\x8aw\xfa\xaa\x17*\x8d'
    #logging
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    app.run(host=host, port=port)
    #to get secret_key in terminal: import os -> os.urandom(24)
