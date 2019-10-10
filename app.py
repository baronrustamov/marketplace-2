from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient()
db = client.Marketplace
marketplace = db.marketplace

@app.route('/')
def index():
    print(marketplace.find())
    print(marketplace.find_one({'_id': ObjectId('5d9e013cf14aea0e5c07544d')}))
    return render_template('index.html')

@app.route('/items/new')
def new_item():
    return render_template('new-item.html')

@app.route('/items/add-new', methods=['POST'])
def add_new_item():
    new_item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('picture')
    }
    product_id = marketplace.insert_one(new_item).inserted_id
    print(product_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
