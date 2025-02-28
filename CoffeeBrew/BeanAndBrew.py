from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, form
from flask_admin.contrib import sqla, rediscli
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt

admin=Admin()
app=Flask(__name__)
app.secret_key='yippee'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/739329/OneDrive - New College Swindon/CoffeeBrew/BrewCoffee.db'

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

bcrypt=Bcrypt(app)
db = SQLAlchemy(app)
admin.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_screen():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('user_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        query = Users.query.filter_by(username=username).first()
        if query is not None:
            flash(f'username "{username}" is already in use, try another one')
            return render_template('register.html')
        else:
            if password == confirm_password:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                u = Users(username = username, password = hashed_password)
                db.session.add(u)
                db.session.commit()
                flash(f'account successfully created!')
                return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        print(user)
        if user is not None:
            is_valid = bcrypt.check_password_hash(user.password, password)
            print(is_valid)
            if is_valid:
                flash(f'welcome to Coffee Brew {username}!')
                session['username'] = username
                login_user(user)
                return redirect('/home')
            else:
                flash(f'incorrect username or password')
                return render_template('login.html')
        else:
            flash(f'incorrect username or password')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/profile')
def profile():
    username = current_user.username

@app.route('/logout')
def logout():
    logout_user()
    flash(f'user logged out successfully')
    return redirect('/')
        
class UserAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'

admin.add_view(UserAdminView(Users, db.session))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)