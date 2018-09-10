from wtforms.widgets import TextArea
from wtforms.fields import StringField
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, HiddenField
from wtforms.validators import Required

class DataForm(FlaskForm):
    body = StringField(u'Body', widget=TextArea(), validators = [Required()])

class TemForm(FlaskForm):
    mantemp = StringField(u'Text', widget=TextArea(), validators = [Required()])
    input = StringField(u'Input', widget=TextArea())
    
class TempTemplate(FlaskForm):
    temp_template = HiddenField(u'temp_template', validators = [Required()])
    
class TempHeader(FlaskForm):
    header_list = HiddenField(u'header_list')

class TempString(FlaskForm):
    string_list = HiddenField(u'string_list')