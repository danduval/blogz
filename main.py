from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'y337kGcys&zP3B'

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref='owner')

    def __init__(self, user, password):
        self.user = user
        self.password = password

@app.route('/blog', methods=["POST", "GET"])
def index():

    if request.method == "POST":
        # validate first:
        title = request.form['title']
        body = request.form['body']
        owner = request.form['owner']
        
        error = False
        error_1 = ''
        error_2 = ''
        error_3 = ''

        if title == '':
            error = True
            error_1 = "Please enter a title"

        if owner == '':
            error = True
            error_2 = 'Please enter your username'

        if body == '':
            error = True
            error_3 = "Please enter a blog post"

        if error == True:
            return render_template('new-post.html', error_1=error_1, error_2=error_2, error_3=error_3, body=body, title=title, owner=owner)

        else:
            owner = User.query.filter_by(user=owner).first()
            blog = Blog(title, body, owner)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog?id=' + str(blog.id))

    
    
    if not request.args:
        blogs = Blog.query.all()
        return render_template("blog.html", blogs=blogs)

    else:
        id = request.args.get('id')
        blogs = Blog.query.filter_by(id=id).all()
        return render_template("blog.html", blogs=blogs)

    

@app.route('/new_post')
def new_post():
    return render_template('new-post.html')

@app.route('/signup', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        verification = request.form['verification']

        # TODO - validate user's data

        error = False
        error_1 = ''
        error_2 = ''
        error_3 = ''
        error_4 = ''
        error_5 = ''

        # User leaves any of the username, password, or verify fields blank and gets an error message that one or more fields are invalid.

        if user == '' or password == '' or verification == '':
            error_1 = 'Please fill out all fields'
            error = True

        # User enters a username that already exists and gets an error message that username already exists.

        existing_user = User.query.filter_by(user=user).first()
        if user == existing_user:
            error_2 = 'User already exists, select a different username'
            error = True

        # hmmm ... why doesn't the above error message work?  All of the other ones do ...

        # User enters different strings into the password and verify fields and gets an error message that the passwords do not match.

        if password != verification:
            error_3 = 'password and verification do not match'
            error = True
    
        # User enters a password or username less than 3 characters long and gets either an invalid username or an invalid password message.

        if len(user) > 0 and len(user) < 3 :
            error_4 = "Username must be at least 3 characters long"
            error = True

        if len(password) > 0 and len(password) < 3:
            error_5 = "Password must be at least 3 characters long"
            error = True

        # If we have an error, redirect to "signup" and display error messages

        if error == True:
            errors = []
            errors.append(error_1)
            errors.append(error_2)
            errors.append(error_3)
            errors.append(error_4)
            errors.append(error_5)

            return render_template("signup.html", errors=errors, user=user)

    # User enters new, valid username, a valid password, and verifies password correctly and is redirected to the '/newpost' page with their username being stored in a session.

        if not existing_user:
            new_user = User(user, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = user
            return redirect('/new_post')

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    error_1 = ''
    error_2 = ''

    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        user = User.query.filter_by(user=username).first()

    # User enters a username that is stored in the database with the correct password and is redirected to the /newpost page with their username being stored in a session.

        if user and user.password == password:
            session['user'] = username
            return redirect('/new_post')

    # ok that one seems to work

    # User enters a username that is stored in the database with an incorrect password and is redirected to the /login page with a message that their password is incorrect.

        if user and user.password != password:
            error_1 = "Incorrect password"
            return render_template("login.html", error=error_1)

    # that one also seems good

    # User tries to login with a username that is not stored in the database and is redirected to the /login page with a message that this username does not exist.

        if not user:
            error_2 = "Username does not exist"
            return render_template("login.html", error=error_2)

    # this also seems copacetic

    # User does not have an account and clicks "Create Account" and is directed to the /signup page.

    # uh ... what?  We're not dealing with "Create Account" here ... is this instruction an error?

    return render_template('login.html')

if __name__ == '__main__':
    app.run()