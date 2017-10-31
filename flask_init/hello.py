import os
import sys
from flask import Flask, url_for, request, render_template, redirect, flash, make_response
app = Flask(__name__)

@app.route('/login3', methods=['GET', 'POST']) #using cookies
def login3():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            response = make_response(redirect(url_for('welcome')))
            response.set_cookie('username', request.form.get('username'))
            flash("Succesfully logged in")
            return response
        else:
            error = 'Incorrect username and password'
    return render_template('login3.html', error=error)
    
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
    if (username == password):
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
    app.secret_key = 'simple_super_secret_key' #for flashing messages
    app.run(host=host, port=port)
