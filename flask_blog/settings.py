import os

SECRET_KEY = 'dsgjklfgkjfkgjfkgj456464646'
DEBUG = True
DB_USERNAME = 'root'
DB_PASSWORD = 'a6771330'
BLOG_DATABASE_NAME = 'blog'
DB_HOST = os.getenv('IP', '0.0.0.0')
DB_URI = 'mysql+pymysql://%s:%s@%s/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, BLOG_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_IMAGES_DEST = '/home/pi/PythonStudy/flask_blog/uploads'
UPLOADED_IMAGES_URL = '/flask_blog/uploads'