from flask import Flask, render_template, request, redirect, jsonify
from cls import classify,message_type,question_response
import sqlite3
import os
import json
import time
from datetime import datetime

app = Flask(__name__)

# Create database connection
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ensure the database and table exist
with app.app_context():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, category VARCHAR(255), cost INT, description TEXT, date DATE);")
    con.commit()
    con.close()

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/getMessageDetails', methods=['POST'])
def get_message_details():
    data = request.get_json()
    message = data.get('msg', '')
    msg_type = message_type(message).strip()

    if msg_type == "classify":
        response_from_model = eval(classify(message))
        cost = response_from_model["cost"]
        category = response_from_model["category"]
        return jsonify({'category': category, 'cost': cost, 'message': message})
    
    if msg_type == "generic":
        conn = sqlite3.connect('data.db')
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM expenses").fetchall()
        json_format_dump = json.dumps([dict(x) for x in rows])
        response_from_model = question_response(message, json_format_dump)
        return jsonify({'category': "", 'cost': "", 'message': response_from_model})
    
    return jsonify({'category': "", 'cost': "", 'message': "Sorry, I didn't understand the message."})
    
@app.route('/addToDatabase', methods=['POST'])
def add_to_database():
    category = request.form['category']
    cost = request.form['cost']
    message = request.form['message']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, cost, description, date) VALUES (?, ?, ?, ?)",
                   (category, cost, message,datetime.today().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()
    return "Added to the database."

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

# Run the Flask app
if __name__ == "__main__":
    app.run()
