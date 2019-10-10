from app import app
import re

client = app.test_client()
app.config['TESTING'] = True

sample_product = {
    'title': 'Sham Wow',
    'description': 'Wash, clean, and dry any surface!',
    'picture': 'http://assets.nydailynews.com/polopoly_fs/1.1455925.1379167741!/img/httpImage/image.jpg_gen/derivatives/article_750/shamwow15n-1-web.jpg',
    'price': '19.95$'
}

mod_sample_product = {
    'title': 'Sham Wow!',
    'description': 'Wash, clean, and dry any surface! Get yours today!',
    'picture': 'http://media3.s-nbcnews.com/j/streams/2013/september/130906/8c8881134-shamwowguy.nbcnews-fp-1200-800.jpg',
    'price': '19.99$'
}

def test_index():
    result = client.get('/')
    assert result.status == '200 OK'
    assert b'Marketplace' in result.data
    assert b'List an item' in result.data

def test_new_product():
    result = client.get('products/new')
    assert result.status == '200 OK'
    assert b'Enter the title of your product' in result.data

def test_CRUD_product():
    # Create
    result = client.post('/products/add-new', data=sample_product)
    assert result.status == '302 FOUND'
    assert b'Redirecting...' in result.data
    sample_product_id = re.search('<a href="/products/(.*)">', str(result.data)).group(1)

    # Read
    result = client.get('products/'+sample_product_id)
    assert result.status == '200 OK'
    assert bytes(sample_product['title'], 'utf-8') in result.data
    assert bytes(sample_product['description'], 'utf-8') in result.data
    assert bytes(sample_product['picture'], 'utf-8') in result.data
    assert bytes(sample_product['price'], 'utf-8') in result.data

    # Update
    result = client.get('products/'+sample_product_id+'/edit')
    assert b'Modify the title of your product' in result.data

    result = client.post('/products/'+sample_product_id+'/edit-in-db', data=mod_sample_product)
    assert result.status == '302 FOUND'

    result = client.get('products/'+sample_product_id)
    assert result.status == '200 OK'
    assert bytes(mod_sample_product['title'], 'utf-8') in result.data
    assert bytes(mod_sample_product['description'], 'utf-8') in result.data
    assert bytes(mod_sample_product['picture'], 'utf-8') in result.data
    assert bytes(mod_sample_product['price'], 'utf-8') in result.data

    # Delete
    result = client.get('/products/'+sample_product_id+'/delete')
    assert result.status == '302 FOUND'

    result = client.get('products/'+sample_product_id)
    assert bytes(mod_sample_product['title'], 'utf-8') not in result.data
    assert bytes(mod_sample_product['description'], 'utf-8') not in result.data
    assert bytes(mod_sample_product['picture'], 'utf-8') not in result.data
    assert bytes(mod_sample_product['price'], 'utf-8') not in result.data
