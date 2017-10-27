
import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'
    
if __name__ == '__main__':
    host = '0.0.0.0'
    port = 55000
    app.run(host=host, port=port)