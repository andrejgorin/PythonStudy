
import os
from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return 'index page'

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
    app.run(host=host, port=port)