from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
from sqlalchemy.sql import text
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/store_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# ---------------------- Models ----------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('manager', 'cashier'), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    low_stock_threshold = db.Column(db.Integer, default=5)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    cashier_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date_sold = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product')
    customer = db.relationship('Customer')
    cashier = db.relationship('User')


with app.app_context():
    db.create_all()


# ---------------------- Authentication ----------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ---------------------- User Routes ----------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        role = request.form['role']

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ---------------------- Dashboard ----------------------

@app.route('/')
@login_required
def dashboard():
    return render_template('index.html', role=session.get('role'))


# ---------------------- Product Routes ----------------------

@app.route('/products')
@login_required
def view_products():
    products = Product.query.all()
    return render_template('view_products.html', products=products)


@app.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if session.get('role') != 'manager':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        existing_product = Product.query.filter_by(name=name).first()
        if existing_product:
            existing_product.stock += stock
        else:
            new_product = Product(name=name, price=price, stock=stock)
            db.session.add(new_product)

        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('view_products'))

    return render_template('add_product.html')


# ---------------------- Customer ----------------------

@app.route('/customers')
@login_required
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)


# ---------------------- Sales ----------------------

@app.route('/sales', methods=['GET', 'POST'])
@login_required
def record_sale():
    if session.get('role') not in ['cashier', 'manager']:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity_sold[]')
        cashier_id = session.get('user_id')

        customer = Customer.query.filter_by(phone=customer_phone).first()
        if not customer:
            customer = Customer(name=customer_name, phone=customer_phone)
            db.session.add(customer)
            db.session.commit()

        total_price = 0
        sales = []
        insufficient_stock = False

        for product_id, quantity in zip(product_ids, quantities):
            quantity = int(quantity)
            product = Product.query.get(product_id)

            if product and product.stock >= quantity:
                total_price += product.price * quantity
                sales.append(Sale(
                    product_id=product.id,
                    customer_id=customer.id,
                    cashier_id=cashier_id,
                    quantity_sold=quantity,
                    total_price=product.price * quantity
                ))
            else:
                insufficient_stock = True
                flash(f'Insufficient stock for {product.name}!', 'danger')

        if insufficient_stock:
            db.session.rollback()
            return redirect(url_for('record_sale'))

        for sale in sales:
            product = Product.query.get(sale.product_id)
            product.stock -= sale.quantity_sold

        db.session.add_all(sales)
        db.session.commit()

        flash(f'Sale recorded successfully! Total: Rs.{total_price:.2f}', 'success')
        return redirect(url_for('bill', sale_id=sales[-1].id))

    products = Product.query.all()
    return render_template('sales.html', products=products)


@app.route('/bill/<int:sale_id>')
@login_required
def bill(sale_id):
    sale = db.session.query(Sale, Product, Customer, User) \
        .join(Product, Sale.product_id == Product.id) \
        .join(Customer, Sale.customer_id == Customer.id) \
        .join(User, Sale.cashier_id == User.id) \
        .filter(Sale.id == sale_id).first()

    if not sale:
        flash('Sale not found', 'danger')
        return redirect(url_for('sales_history'))

    sale, product, customer, cashier = sale
    return render_template('bill.html', sale=sale, product=product, customer=customer, cashier=cashier)


@app.route('/sales_history')
@login_required
def sales_history():
    if session.get('role') != 'manager':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))

    search_query = request.args.get('search', '')

    sales = db.session.query(Sale, Customer, Product) \
        .join(Customer, Sale.customer_id == Customer.id) \
        .join(Product, Sale.product_id == Product.id) \
        .order_by(Sale.id.asc())

    if search_query:
        sales = sales.filter(
            Customer.name.ilike(f"%{search_query}%") |
            Customer.phone.ilike(f"%{search_query}%")
        )

    sales = sales.all()
    return render_template('sales_history.html', sales=sales)


# ---------------------- Inventory ----------------------

@app.route('/inventory')
@login_required
def inventory():
    products = Product.query.all()
    return render_template('inventory.html', products=products)


# ---------------------- Admin Setup ----------------------

@app.route('/setup_admin')
def setup_admin():
    existing_admin = User.query.filter_by(username='admin').first()
    if not existing_admin:
        hashed_password = bcrypt.generate_password_hash("admin123").decode('utf-8')
        admin = User(username="admin", password=hashed_password, role="manager")
        db.session.add(admin)
        db.session.commit()
        return "Admin created! Username: admin, Password: admin123"
    return "Admin already exists!"


# ---------------------- Sales & Inventory Analysis ----------------------

@app.route('/sales_inventroy_analysis')
@login_required
def sales_inventory_analysis():
    if session.get('role') != 'manager':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))

    daily_sales = db.session.execute(text(
        "SELECT SUM(total_price) FROM sale WHERE date_sold >= CURDATE()"
    )).scalar() or 0

    weekly_sales = db.session.execute(text(
        "SELECT SUM(total_price) FROM sale WHERE date_sold >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
    )).scalar() or 0

    monthly_sales = db.session.execute(text(
        "SELECT SUM(total_price) FROM sale WHERE date_sold >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)"
    )).scalar() or 0

    total_stock_value = db.session.execute(text(
        "SELECT SUM(stock * price) FROM product"
    )).scalar() or 0

    low_stock_products = db.session.execute(text(
        "SELECT * FROM product WHERE stock <= low_stock_threshold"
    )).fetchall()

    return render_template('sales_inventory_analysis.html',
                           daily_sales=daily_sales,
                           weekly_sales=weekly_sales,
                           monthly_sales=monthly_sales,
                           total_stock_value=total_stock_value,
                           low_stock_products=low_stock_products)


if __name__ == '__main__':
    app.run(debug=True)
