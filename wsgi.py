# wsgi.py

from flask import Flask, request, render_template
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

@app.route('/')
def hello():
    return "Hello World!"

# LIST
@app.route('/products')
def list_products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
#    products = db.session.query(Product).order_by(Product.name).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

# READ
@app.route('/products/<int:prod_id>')
def get_product(prod_id):
    product = db.session.query(Product).get(prod_id)
    if product == None:
        abort(404)
    return product_schema.jsonify(product)

# ADD
@app.route('/products', methods=['POST'])
def add_product():
    name = Product(name=request.form['name'])
    print(name)
    product = db.session.add(name)
    db.session.commit()
    return product_schema.jsonify(product)

# DELETE
@app.route('/products/<int:prod_id>', methods=['DELETE'])
def del_product(prod_id):
    product = db.session.query(Product).get(prod_id)
    db.session.delete(product)
    db.session.commit()

# PATCH
@app.route('/products/<int:prod_id>', methods=['PATCH'])
def upd_product(prod_id):
    produit = db.session.query(Product).get(prod_id)
    rf_name = request.form['name']
#    text = Product(text=request.form['text'])
#    print(f"name = {name}, text = {text}")
    produit.name = rf_name
#    Product.text = text
#    return product_schema.jsonify(product)
    #product = db.session.add(name)
    db.session.commit()
    return product_schema.jsonify(produit)
