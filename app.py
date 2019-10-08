from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items/new')
def new_item():
    return render_template('new-item.html')

if __name__ == '__main__':
    app.run(debug=True)
