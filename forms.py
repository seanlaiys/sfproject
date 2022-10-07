from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

# Form for searching users by name
class SearchForm(Form):
  search = StringField('Search for Users:', [DataRequired()])