from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flaskext.markdown import Markdown
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

# migrations
migrate = Migrate(app, db)

# Markdown
Markdown(app)

#images
uploaded_images = UploadSet('images', IMAGES)
configure_uploads(app, uploaded_images)

from blog import views
from author import views