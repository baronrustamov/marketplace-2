from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient()
db = client.Marketplace
marketplace = db.marketplace

@app.route('/')
def index():
    return render_template('index.html', products=marketplace.find())

@app.route('/products/new')
def new_product():
    return render_template('new-product.html')

@app.route('/products/add-new', methods=['POST'])
def add_new_product():
    new_product = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('picture')
    }
    product_id = marketplace.insert_one(new_product).inserted_id
    return redirect('/products/'+str(product_id))

@app.route('/products/<product_id>')
def show_product(product_id):
    return render_template('show-product.html', product = marketplace.find_one({'_id': ObjectId(product_id)}))

@app.route('/products/<product_id>/edit')
def edit_product(product_id):
    return render_template('edit-product.html', product = marketplace.find_one({'_id': ObjectId(product_id)}))

@app.route('/products/<product_id>/edit-in-db', methods=['POST'])
def edit_product_in_db(product_id):
    modified_product = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('picture')
    }
    marketplace.update({'_id': ObjectId(product_id)}, modified_product)
    return redirect('/products/'+product_id)

@app.route('/products/<product_id>/delete')
def delete_product(product_id):
    marketplace.remove({'_id': ObjectId(product_id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
