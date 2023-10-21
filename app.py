# app.py
from flask import Flask, request, jsonify, redirect, render_template
from flask import Flask, request, jsonify, redirect, render_template, g

import sqlite3
import random
import string

app = Flask(__name__)

# Initialize SQLite database
conn = sqlite3.connect('urls.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS url_mappings (id INTEGER PRIMARY KEY, long_url TEXT, short_url TEXT)')
conn.commit()

# Function to generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    short_url = generate_short_url()

    # Create a new database connection for this request
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    # Perform the database operation
    cursor.execute('INSERT INTO url_mappings (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
    conn.commit()

    # Close the database connection
    conn.close()

    return jsonify({'short_url': short_url})


@app.route('/<short_url>')
def redirect_to_original(short_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    cursor.execute('SELECT long_url FROM url_mappings WHERE short_url = ?', (short_url,))
    result = cursor.fetchone()

    if result:
        long_url = result[0]
        conn.close()  # Close the connection
        return redirect(long_url)
    else:
        conn.close()  # Close the connection
        return "URL not found"

# Function to create a new database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('urls.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/list_urls')
def list_urls():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT long_url, short_url FROM url_mappings')
    rows = cursor.fetchall()
    urls = [{'long_url': row['long_url'], 'short_url': row['short_url']} for row in rows]
    return jsonify(urls)


if __name__ == '__main__':
    app.run(debug=True)
