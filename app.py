# app.py
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from models import init_db

app = Flask(__name__)
app.secret_key = 'secret-key'  # for session

init_db()

# --- Helper Functions ---

@app.context_processor
def inject_now():
    return {'year': datetime.now().year}

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def recommend_products(current_product):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id != ?', (current_product['id'],))
    all_products = cursor.fetchall()
    conn.close()

    recommendations = []
    for product in all_products:
        score = 0
        if product['category'] == current_product['category']:
            score += 2
        if abs(product['price'] - current_product['price']) <= 10:
            score += 1
        if set(product['tags'].split(',')) & set(current_product['tags'].split(',')):
            score += 1
        if score > 0:
            recommendations.append((product, score))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in recommendations[:3]]

# --- Routes ---

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    
    if not product:
        return 'Product not found', 404

    # Store in session for 'recently viewed'
    viewed = session.get('recently_viewed', [])
    if product_id not in viewed:
        viewed.insert(0, product_id)
        session['recently_viewed'] = viewed[:5]

    recommendations = recommend_products(product)
    return render_template('product_detail.html', product=product, recommendations=recommendations)

@app.route('/add', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        tags = request.form['tags']
        description = request.form['description']

        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, price, category, tags, description) VALUES (?, ?, ?, ?, ?)',
                     (name, price, category, tags, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('product_form.html', action="Add")

@app.route('/edit/<int:product_id>', methods=('GET', 'POST'))
def edit_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        tags = request.form['tags']
        description = request.form['description']

        conn.execute('UPDATE products SET name = ?, price = ?, category = ?, tags = ?, description = ? WHERE id = ?',
                     (name, price, category, tags, description, product_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('product_form.html', product=product, action="Edit")

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/recent')
def recently_viewed():
    ids = session.get('recently_viewed', [])
    conn = get_db_connection()
    placeholders = ','.join('?' for _ in ids)
    products = conn.execute(f'SELECT * FROM products WHERE id IN ({placeholders})', ids).fetchall()
    conn.close()
    return render_template('index.html', products=products, title="Recently Viewed")

if __name__ == '__main__':
    app.run(debug=True)
