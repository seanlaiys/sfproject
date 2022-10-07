from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(Form):
  search = StringField('Search for Users:', [DataRequired()])