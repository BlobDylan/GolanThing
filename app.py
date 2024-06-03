# Import necessary libraries
from flask import Flask, render_template, request, redirect, jsonify
from cls import classify
import os
import time


# Create a Flask web application
app = Flask(__name__)

# Function to get a response from the chatbot
def get_response(userText):
    return "response!"

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_response(userText))

@app.route('/getMessageDetails', methods=['POST'])
def get_message_details():
    data = request.get_json()
    message = data.get('msg', '')
    response_from_model = eval(classify(message))
    cost = response_from_model["cost"]
    category = response_from_model["category"]
    return jsonify({'category': category, 'cost': cost, 'message' : message})

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

# Run the Flask app
if __name__ == "__main__":
    app.run()