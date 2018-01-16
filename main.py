from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:mynewblog77@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))
     

    def __init__(self, title, body):
        self.title= title
        self.body= body


@app.route('/', methods=['GET'])
def blog():  
    blogs = Blog.query.all()
    return render_template('main.html', blogs = blogs)

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    blog_title=""  
    blog_body=""
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        if(not blog_title) or (blog_title.strip()==""):
            flash('Please specify the title', 'error')
        elif(not blog_body) or (blog_body.strip()==""):
            flash('Please specify your entry', 'error')
        elif(len(blog_title)!= 0) and (len(blog_body)!= 0):
            blog = Blog(title=blog_title, body=blog_body)
            db.session.add(blog)
            db.session.commit()
            return render_template('entry-confirmation.html', title= blog_title, blog=blog)
            #return redirect('/')
       
    return render_template('addpost.html', blog_title=blog_title, blog_body=blog_body)


@app.route('/viewentry', methods=['GET','POST'])
def viewentry():
    # to revise
    if request.method == 'GET':
        view_id= int(request.args.get('id'))

        blog = Blog.query.get(view_id)
        if blog:
            return render_template('entry-confirmation.html', blog=blog)
        else: 
            flash("This blog no longer exists", 'error')
      
    return redirect('/')
    

if __name__ == '__main__':
    app.run()