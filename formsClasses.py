from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea


# for Loginform
class Loginform(FlaskForm):
    username =  StringField("Username", validators=[DataRequired()])
    User_password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField()


#create flask form class
class NameerForm(FlaskForm):
    name = StringField("what is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

#for testpwd
class TestForm(FlaskForm):
    email = StringField("what is your email", validators=[DataRequired()])
    password = PasswordField("enter your password",validators=[DataRequired()])
    submit = SubmitField("Submit")

#user form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("favorite_color")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Password much mach')])
    password_hash2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")
