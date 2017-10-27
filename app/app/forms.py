from wtforms.widgets import TextArea
from wtforms.fields import StringField
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class ContactForm(FlaskForm):
    body = StringField(u'Body', widget=TextArea(), validators = [Required()])

class TemForm(FlaskForm):
    mantemp = StringField(u'Text', widget=TextArea(), validators = [Required()])
    input = StringField(u'Input', widget=TextArea())
