from flask import Flask, render_template, redirect, \
 request, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/login'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SECRET_KEY'] ='01656235a4bda1c01b1c45a7fe1f3cbc'

db = SQLAlchemy(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form.get('username')
            password = request.form.get('password')
            row = db.session.execute( "Select username,password FROM users WHERE username=:username AND password=:password",{"username":username, "password":password}).fetchone()
            print(row)
            if row:
                session['loginsuccess'] = True
                return redirect (url_for('profile'))
            else:
                return redirect (url_for('index'))
            
        else:
            return "You must provide a username and password"
    else:
        return render_template('login.html')

@app.route('/new')
def new_user():
    if request.method == 'POST':
        pass

    return render_template('register.html')

@app.route('/register',methods = ["GET","POST"])
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('profile.html')

@app.route('/profile')
def profile():
    if session['loginsuccess'] == True:
        return render_template('profile.html')
    return render_template('profile.html')




if __name__ == '__main__':
    app.run()