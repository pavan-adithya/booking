from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'tickets.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute('''CREATE TABLE tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            event TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book_ticket():
    data = request.get_json()
    name = data.get('name')
    event = data.get('event')
    quantity = data.get('quantity')
    if not name or not event or not quantity:
        return jsonify({'error': 'Missing data'}), 400
    conn = get_db_connection()
    conn.execute('INSERT INTO tickets (name, event, quantity) VALUES (?, ?, ?)', (name, event, quantity))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Ticket booked successfully'})

@app.route('/tickets', methods=['GET'])
def get_tickets():
    conn = get_db_connection()
    tickets = conn.execute('SELECT * FROM tickets').fetchall()
    conn.close()
    return jsonify([dict(ticket) for ticket in tickets])

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 