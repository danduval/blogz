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
        # validate first:
        title = request.form['title']
        body = request.form['body']
        
        error = False
        error_1 = ''
        error_2 = ''

        if title == '':
            error = True
            error_1 = "Please enter a title"

        if body == '':
            error = True
            error_2 = "Please enter a blog post"

        if error == True:
            return render_template('new-post.html', error_1=error_1, error_2=error_2, body=body)

        else:
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog?id=' + str(blog.id))

    blogs = Blog.query.all()
    
    if not request.args:
        return render_template("blog.html", blogs=blogs)

    else:
        id = request.args.get('id')
        blogs = Blog.query.filter_by(id=id).all()
        return render_template("blog.html", blogs=blogs)

    

@app.route('/new_post')
def new_post():
    return render_template('new-post.html')

if __name__ == '__main__':
    app.run()