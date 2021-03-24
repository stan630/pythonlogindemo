from flask import Flask, render_template, redirect, \
 request, session, url_for, flash
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, logout_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/login'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SECRET_KEY'] ='01656235a4bda1c01b1c45a7fe1f3cbc'

db = SQLAlchemy(app)

login = LoginManager()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(32), index=True, unique=True)
    

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form.get('username')
            password = request.form.get('password')
            row = db.session.execute( "SELECT username,password FROM users WHERE username=:username AND password=:password",{"username":username, "password":password}).fetchone()
            print(row)
            if row:
                session['username'] = username
                flash("You are logged in as" + ' '  + username.upper(), "success")
                return render_template('profile.html')
            else:
                flash ("You entered an incorrect username and/or password!", "warning")
                return redirect (url_for('index'))
            
        else:
            flash ("You must provide a username and password","warning")
            return redirect (url_for('index'))
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        rows = db.session.execute( "SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        print(rows)
        if rows:
            flash("Username already exists!","danger")
            return render_template('register.html')
        
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        # print(username, password, email)
        db.session.execute("INSERT INTO users (username, password, email) VALUES (:username,:password,:email)", {"username": username, "password": password, "email": email})
        db.session.commit()
        flash("You are now registered!", "success")
        return redirect(url_for('index'))
    else:
        return render_template('register.html')


@app.route('/login')
def login():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if "username" in session:
        username = session["username"]
        
        return render_template('profile.html')
    return render_template('profile.html')




if __name__ == '__main__':
    app.run()