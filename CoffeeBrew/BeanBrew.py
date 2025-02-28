from datetime import datetime
from flask import *
from flask_sqlalchemy import *
from flask_admin import Admin, form
from flask_admin.contrib import sqla, rediscli
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt

admin=Admin()
app=Flask(__name__)
app.secret_key='yippee'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/740424/OneDrive - New College Swindon/CoffeeBrew/BrewCoffee.db'

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


class Menu(db.Model):
    itemid=db.Column(db.Integer, primary_key=True)
    item_name=db.Column(db.String, unique=True, nullable=False)
    item_price=db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.String, nullable=False)


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_screen():
    return render_template('home.html')

@app.route('/store', methods=['GET','POST'])
def store():
    menu=Menu.query.all()
    return render_template('store.html', menu=menu)

@app.route('/order/add/<product_ordered>')
def add_to_order(product_ordered):
    products=Menu.query.all()

    if "order" not in session:
        session["order"]=[]
    for product in products:   #fixed error where items were not added to order
        if product.item_name == product_ordered:
            session["order"].append({"name":product.item_name, "price": product.item_price})
            flash(f'{product.item_name} was successfully added to your order!')
            return redirect('/store')

@app.route('/order', methods=['GET', 'POST'])
def order_basket():
    order = session.get("order",[])
    subtotal = 0
    for item in order:
        subtotal += (float(item["price"]))
    return render_template("order_basket.html", order_basket=order, subtotal=subtotal)

@app.route('/clear')
def clear_basket():
    session["order"]=[]
    flash(f'your basket was successfully cleared')
    return redirect('/order')

#below is unfixed code where I intended to add a delete item function for admins
'''
@app.route('/delete/<item>', methods=['GET', 'POST'])
def delete_item(item):
    products = Menu.query.filter_by(item_name=item).all()
    for product in products:
        db.session.delete(product)
        db.session.commit()
    flash(f'{item} has been successfully deleted from the database')
    return redirect('/store')
'''
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    order = session.get("order",[])
    subtotal = 0
    for item in order:
        subtotal += (float(item["price"])) #fixed error where price would not be summed 
    return render_template('checkout.html', order_basket=order, subtotal=subtotal)

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

@app.route('/adminmenu', methods = ['GET', 'POST'])
def admin_menu():
    if request.method== 'POST':
        item_name = request.form.get('item_name')
        item_price = request.form.get('item_price')
        item_type = request.form.get('item_type')
        query = Menu.query.filter_by(item_name=item_name).first()
        if query is not None:
            flash(f'{item_name} is already on the menu')
            return render_template('menu.html')
        else:
            M = Menu(item_name=item_name, item_price=item_price, item_type=item_type)
            db.session.add(M)
            db.session.commit()
            flash(f'{item_name} successfully added to menu')
            return render_template('menu.html')
    return render_template('menu.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        if "username" in session:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            db.session.query(Users).filter(Users.username == username).update({'password': password})
            db.session.commit()
            return redirect(url_for('profile'))
        return render_template('update.html')
    return render_template('update.html')
@app.route('/profile')
def profile():
    username = current_user.username
    return render_template('profile.html', username=username)
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