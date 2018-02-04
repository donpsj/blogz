from flask import Flask, request, redirect, render_template, session, flash
from service.hasher import make_hash_from, are_strings_same
from models import User, Blog
from app import app, db

@app.route('/signup', methods=['GET','POST'])
def signup():  
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        verify = str(request.form['verify'])
        if len(username)<3:
           flash('Indalid Username! "' + username + '" The username must have at least 3 characters', 'error')
           return redirect('/signup')
        elif len(username)>20:
           flash('Indalid Username!! "' + username + '" The username cannot have more than 20 characters', 'error')
           return redirect('/signup')
        elif " " in username or username.strip() == "":
           flash('Indalid Username!! "' + username + '" The username contains a <space> character', 'error')
           return redirect('/signup')

        username_db_count = User.query.filter_by(username=username).count()

        if username_db_count > 0:
            flash('Existing Username! "' + username + '" is already taken', 'error')
            return redirect('/signup')
        elif len(password)<3:
            flash('Indalid password! The password must have at least 3 characters', 'error')
            return redirect('/signup')
        elif len(password)>20:
            flash('Indalid password! The password cannot have more than 20 characters', 'error')
            return redirect('/signup')
        elif " " in password:
            flash('Indalid password! The password cannot contain <space>', 'error')
            return redirect('/signup')
        elif password != verify:
            flash('Indalid password! The passwords did not match', 'error')
            return redirect('/signup')
        user = User(username, make_hash_from(password))
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        session['user_name'] = user.username  
        return redirect('/newpost')
    return render_template('signup.html')
    
    
@app.route('/login', methods=['GET','POST'])
def login():  
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and not are_strings_same(password, user.password):
            flash('Your password is incorrect. Please Try again', 'error')
            return redirect('/login')
        elif not user:
            flash('Indalid Username! "' + username + '" does not exist', 'error') 
            return redirect('/login')
        elif user and are_strings_same(password, user.password):
            session['user_name'] = user.username 
            return redirect('/newpost')
     return render_template('login.html')
  
@app.route('/newpost', methods=['POST','GET'])
def newpost():
    blog_title=""  
    blog_body=""
    user_name = session.get("user_name")
    user = User.query.filter_by(username = user_name).first()
    owner_id = user.id
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        if(not blog_title) or (blog_title.strip()==""):
            flash('Please specify the title', 'error')
        elif(not blog_body) or (blog_body.strip()==""):
            flash('Please specify your entry', 'error')
        elif(len(blog_title)!= 0) and (len(blog_body)!= 0):
            blog = Blog(title=blog_title, body=blog_body,owner_id=owner_id)
            db.session.add(blog)
            db.session.commit()
            return render_template('singleUser.html', blog=blog, user=user)
    return render_template('addpost.html')

@app.route('/view_userpost', methods=['GET','POST'])
def view_userpost():
    if request.method == 'GET':
        view_id= int(request.args.get('id'))
        user = User.query.filter_by(id = view_id).first()
        if user:
            owner_id = user.id
            blogs = Blog.query.filter_by(owner_id =user.id).all()
            return render_template('userpost.html', blogs=blogs, user = user) 
                                        
    return redirect('/')

@app.route('/viewentry', methods=['GET','POST'])
def viewentry():
    if request.method == 'GET':
        view_id= request.args.get('id')
        blog = Blog.query.get(view_id)
        if blog:
            owner_id = blog.owner_id
            user = User.query.filter_by(id = owner_id).first()
            if user:
                return render_template('singleUser.html', blog=blog, user = user)
                  
    return redirect('/')

@app.route('/logout')
def logout():
    if session:
        del session['user_name']
    else:
        return redirect('/login')
    return redirect('/blog')


@app.route('/blog', methods=['GET'])
def blog():  
    if request.method == 'GET':
        users=User.query.all()
        blogs = Blog.query.all()
        return render_template('main.html', blogs=blogs, users=users) 
    return redirect('/')

     

@app.route('/', methods=['GET'])
def index(): 
    users = User.query.all()
    return render_template('index.html', users = users)

@app.before_request
def require_login():
    login_requirede_routes = ['newpost','logout']
    if request.endpoint in login_requirede_routes and 'user_name' not in session:
        return redirect('/login')
    app.secret_key = 'A0Zr98j/3yXmerciR~XHH!jmN]LWX/,?RU'

if __name__ == '__main__':
    app.run()