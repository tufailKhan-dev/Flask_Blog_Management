from flask import Flask,render_template, flash
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
# create instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my name is Batman"
# add data base
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#initial lize database
db = SQLAlchemy(app)

#create a model
class Users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable = False)
    email= db.Column(db.String(100),nullable = False, unique = True)
    date_added= db.Column(db.DateTime,default = datetime.now)

    #create sring
    def __repr__(self):
        return '<Name %r>' % self.name

#user form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")



#create flask form class
class NameerForm(FlaskForm):
    name = StringField("what is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


#Filters!!!
#safe
#trim
#striptag
#title
#upper
#lower




@app.route('/user/add', methods=["GET","POST"])
def adduser():
    form_obj = UserForm()

    return render_template("adduser.html", form_obj=form_obj)

@app.route('/')
def main():
    return render_template('index.html')



#create custom error 

#invalid url
@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404


#internal server error
@app.errorhandler(500)
def page_not_found(err):
    return render_template('500.html'), 500



# create form page
@app.route("/form", methods=["GET","POST"])
def form():
    name = None
    form_obj = NameerForm()
    # validate form
    if form_obj.validate_on_submit():
        name = form_obj.name.data
        form_obj.name.data = ''
        flash('Successful submit form', 'success')

    return render_template('form.html', 
                           name=name,
                           form_obj = form_obj)