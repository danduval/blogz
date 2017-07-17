from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=["POST", "GET"])
def index():

    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        blog = Blog(title, body)
        db.session.add(blog)
        db.session.commit()

    blogs = Blog.query.all()
        
    return render_template("blog.html", blogs=blogs)

@app.route('/new_post')
def new_post():
    return render_template('new-post.html')

if __name__ == '__main__':
    app.run()