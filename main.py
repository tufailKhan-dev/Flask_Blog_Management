from flask import Flask,render_template, flash, request
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
# create instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my name is Batman"
# add data base old database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'
# new Mysql database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# new database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:A334390tuffu@localhost/our_users'
app.config['SQLALCHEMY_TRANK_MODIFICATIONS'] = False
#initial lize database
db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app,db)
#create a model
class Users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable = False)
    email= db.Column(db.String(100),nullable = False, unique = True)
    favorite_color = db.Column(db.String(120))
    date_added= db.Column(db.DateTime,default = datetime.now)

    #create sring
    def __repr__(self):
        return '<Name %r>' % self.name

#user form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("favorite_color")
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
    name = None
    form_obj = UserForm()
    if form_obj.validate_on_submit():
        try:
            user = Users.query.filter_by(email=form_obj.email.data).first()
            if user is None:
                user = Users(name=form_obj.name.data, email=form_obj.email.data, favorite_color= form_obj.favorite_color.data)
                db.session.add(user)
                db.session.commit()
        except Exception as e:
            print("error:", e)
        name = form_obj.name.data
        form_obj.name.data = ''
        form_obj.email.data = ''
        form_obj.favorite_color.data = ''
        flash("User Added Successfully!",'success')
    AllUsers = Users.query.order_by(Users.date_added)
    return render_template("adduser.html",
                           form_obj=form_obj,
                            name=name,
                            AllUsers = AllUsers)



@app.route('/')
def main():
    return render_template('index.html')


# Update the record 
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form_obj = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash('updated successfully', 'success')
            return render_template("update.html", form_obj=form_obj,
                                   name_to_update = name_to_update)

        except:
            flash('something error', 'error')
            return render_template("update.html", form_obj=form_obj,
                                   name_to_update = name_to_update)
    else:
        return render_template("update.html", form_obj=form_obj,
                                   name_to_update = name_to_update, id = id)


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form_obj = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("user successfully deleted", 'success')
        AllUsers = Users.query.order_by(Users.date_added)
        return render_template("adduser.html",
                           form_obj=form_obj,
                            name=name,
                            AllUsers = AllUsers)
    except:
        flash('user not deleted', 'error')
    return render_template("adduser.html",
                           form_obj=form_obj,
                            name=name,
                            AllUsers = AllUsers)

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

    return render_template('form.html', name=name, form_obj=form_obj)



