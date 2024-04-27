from flask import Flask,render_template, flash, request
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
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

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    Nameslug = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.now)

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

# add blog post
@app.route('/add-blog-post',methods=['GET','POST'])
def add_blog_post():
    form_obj = PostForm()
    if form_obj.validate_on_submit():
        post = Posts(title=form_obj.title.data,content=form_obj.content.data,author = form_obj.author.data,Nameslug = form_obj.slug.data)
        
        #clear the form
        form_obj.title.data = ''
        form_obj.author.data = ''
        form_obj.content.data = ''
        form_obj.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        #return a message
        flash("Blog Post submitted successfully", 'success')
    return render_template("add_blog_post.html", form_obj=form_obj)


#create a model
class Users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable = False)
    email= db.Column(db.String(100),nullable = False, unique = True)
    favorite_color = db.Column(db.String(120))
    date_added= db.Column(db.DateTime,default = datetime.now)
    #password 
    password_hash = db.Column(db.String(200))
    @property
    def _password(self):
        raise AttributeError('password is not readable attribte')
    
    @_password.setter
    def _password(self, password):
        self.password_hash = generate_password_hash(password)
    
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    #create sring
    def __repr__(self):
        return '<Name %r>' % self.name

#user form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("favorite_color")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Password much mach')])
    password_hash2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Submit")



#create flask form class
class NameerForm(FlaskForm):
    name = StringField("what is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

#for testpwd
class TestForm(FlaskForm):
    email = StringField("what is your email", validators=[DataRequired()])
    password = PasswordField("enter your password",validators=[DataRequired()])
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
                hashpwd = generate_password_hash(form_obj.password_hash.data)   
                user = Users(name=form_obj.name.data, email=form_obj.email.data, favorite_color= form_obj.favorite_color.data, password_hash=hashpwd)
                db.session.add(user)
                db.session.commit()
        except Exception as e:
            print("error:", e)
        name = form_obj.name.data
        form_obj.name.data = ''
        form_obj.email.data = ''
        form_obj.favorite_color.data = ''
        form_obj.password_hash.data = ''
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


@app.route('/testpwd',methods=['GET','POST'])
def testpwd():
    email = None
    password = None
    pw_to_check = None
    passed = None
    test_obj = TestForm()
    if test_obj.validate_on_submit():
        email = test_obj.email.data
        password = test_obj.password.data

        #clear the form
        test_obj.email.data = ''
        test_obj.password.data = ''
        #check user info
        pw_to_check = Users.query.filter_by(email=email).first()
        if pw_to_check:
            #check password hash
            passed = check_password_hash(pw_to_check.password_hash, password)
            return render_template("testpassword.html",passed = passed,email = email, password = password, pw_to_check = pw_to_check, test_obj = test_obj)
        
    return render_template("testpassword.html",passed = passed,email = email, password = password, pw_to_check = pw_to_check, test_obj = test_obj)

#json data
@app.route('/data')
def get_current_date():
    info = {
        'name' : 'tufail',
        'mname' : 'khan'
    }
    return info
