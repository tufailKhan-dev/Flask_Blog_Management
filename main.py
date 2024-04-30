from flask import Flask, redirect,render_template, flash, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import LoginManager, UserMixin, login_user,login_required,logout_user,current_user
from formsClasses import *
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
class Users(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    name = db.Column(db.String(100),nullable = False)
    email= db.Column(db.String(100),nullable = False, unique = True)
    favorite_color = db.Column(db.String(120))
    date_added= db.Column(db.DateTime,default = datetime.now)
    #password 
    password_hash = db.Column(db.String(200))
    #users can have many post
    posts=db.relationship('Posts', backref='poster')

    @property
    def _password(self):
        raise AttributeError('password is not readable attribte')
    
    @_password.setter
    def _password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    #author = db.Column(db.String(255))
    Nameslug = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.now)
    #foreign key to link users (refer to primary key)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #create sring
    # def __repr__(self):
    #     return '<Name %r>' % self.name





#Filters!!!
#safe
#trim
#striptag
#title
#upper
#lower

@app.context_processor
def base():
    form_obj = SearchForm()
    return dict(form_obj=form_obj)


@app.route('/search', methods = ['POST'])
def SearchBlog():
    form_obj = SearchForm()
    posts = Posts.query
    if form_obj.validate_on_submit():
        search = form_obj.search.data
        posts = posts.filter(Posts.content.like('%' + search + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template('search.html', form_obj = form_obj, search=search, blogs = posts)


""" login start """
#Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/login", methods = ["GET", "POST"])
def login():
    form_obj = Loginform()
    if form_obj.validate_on_submit():
        user = Users.query.filter_by(username=form_obj.username.data).first()

        if user:
            if check_password_hash(user.password_hash, form_obj.User_password.data):
                login_user(user)
                flash('login successfully ', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash("wrong password", 'error')
        else:
            flash(" that user not exits- Try again later", 'error')

    return render_template("login.html", form_obj=form_obj)


""" login end """
""" logout start """

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('you logout successfully', 'success')
    return redirect(url_for('login'))



""" logout end """


""" dashboard start """

@app.route("/dashboard", methods = ["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")

""" dashboard end """




""" blog start """
# add blog post
@app.route('/add-blog-post',methods=['GET','POST'])
@login_required
def add_blog_post():
    form_obj = PostForm()
    if form_obj.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form_obj.title.data,content=form_obj.content.data,poster_id=poster,Nameslug = form_obj.slug.data)
        
        #clear the form
        form_obj.title.data = ''
        form_obj.content.data = ''
        form_obj.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        #return a message
        flash("Blog Post submitted successfully", 'success')
    return render_template("add_blog_post.html", form_obj=form_obj)

# show blogs:
@app.route('/showblog')
def Show_Blog():
    Allblog = Posts.query.order_by(Posts.date_posted)
    return render_template("Blog.html", Allblog=Allblog)

@app.route('/blog/<int:id>')
def blog(id):
    blog = Posts.query.get_or_404(id)
    return render_template("singleblog.html",blog=blog)

#delete blog
@app.route('/blog/delete/<int:id>')
@login_required
def deleteblog(id):
    blog = Posts.query.get_or_404(id)
    id= current_user.id
    if id == blog.poster.id:
        try:
            db.session.delete(blog)
            db.session.commit()
            flash('blog has been deleted', 'success')
            Allblog = Posts.query.order_by(Posts.date_posted)
            return render_template('Blog.html', Allblog=Allblog)
        except Exception as err:
            print("Error:", err)
            flash("blog not hasbeen deleted", 'error')
    else:
        flash('u can not delete this posts', 'error')
        Allblog = Posts.query.order_by(Posts.date_posted)
        return render_template('Blog.html', Allblog=Allblog)



#editblog
@app.route('/blog/edit/<int:id>', methods = ['GET', 'POST'])
def editblog(id):
    blog = Posts.query.get_or_404(id)
    id = current_user.id
    if id == blog.poster.id:
        form_obj = PostForm()
        if form_obj.validate_on_submit():
            blog.title = form_obj.title.data
            blog.content = form_obj.content.data
            blog.Nameslug = form_obj.slug.data
            #update DAtabase
            db.session.add(blog)
            db.session.commit()
            flash("Post has been updated")
            return redirect(url_for('blog',id = blog.id))
        form_obj.title.data = blog.title
        form_obj.slug.data = blog.Nameslug
        form_obj.content.data = blog.content
        return render_template("edit_blog.html", form_obj=form_obj)
    else:
        flash('u can not edit this blog', 'error')
        return redirect(url_for('Show_Blog'))

""" blog end """

@app.route('/user/add', methods=["GET","POST"])
def adduser():
    name = None
    form_obj = UserForm()
    if form_obj.validate_on_submit():
        try:
            user = Users.query.filter_by(email=form_obj.email.data).first()
            if user is None:
                hashpwd = generate_password_hash(form_obj.password_hash.data)   
                user = Users(name=form_obj.name.data,username=form_obj.username.data, email=form_obj.email.data, favorite_color= form_obj.favorite_color.data, password_hash=hashpwd)
                db.session.add(user)
                db.session.commit()
        except Exception as e:
            print("error:", e)
        name = form_obj.name.data
        form_obj.name.data = ''
        form_obj.email.data = ''
        form_obj.username.data = ''
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
@login_required
def update(id):
    form_obj = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
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
@login_required
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
