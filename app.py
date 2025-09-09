from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import json
import os
from config import MONGODB_URI, DB_NAME, COLLECTION_NAME

app = Flask(__name__)

# MongoDB Atlas connection
try:
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to MongoDB Atlas successfully")
except Exception as e:
    print(f"Error connecting to MongoDB Atlas: {e}")

# JSON file path
DATA_FILE = 'data.json'

def read_data_from_file():
    """Read data from JSON file"""
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"error": "Data file not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON data"}

@app.route('/api', methods=['GET'])
def api_route():
    """API endpoint that returns data from JSON file"""
    data = read_data_from_file()
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page with form for data submission"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            # Validate required fields
            if not name or not email:
                return render_template('index.html', 
                                     error="Name and email are required fields")
            
            # Create document to insert
            document = {
                'name': name,
                'email': email,
                'message': message
            }
            
            # Insert into MongoDB Atlas
            result = collection.insert_one(document)
            
            # Redirect to success page
            return redirect(url_for('success'))
            
        except Exception as e:
            # Return error message if insertion fails
            return render_template('index.html', 
                                 error=f"Error submitting data: {str(e)}")
    
    # GET request - show the form
    return render_template('index.html')

@app.route('/success')
def success():
    """Success page after form submission"""
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
