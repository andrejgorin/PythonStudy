from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

from blog import views
from author import views

# migrations
migrate = Migrate(app, db)

# Markdown
Markdown(app)

