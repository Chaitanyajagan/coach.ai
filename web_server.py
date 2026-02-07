from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/login', methods=['POST'])
def login():
    """API endpoint for login"""
    # This will integrate with your existing database
    return {'status': 'success', 'message': 'Login successful'}

@app.route('/api/signup', methods=['POST'])
def signup():
    """API endpoint for signup"""
    # This will integrate with your existing database
    return {'status': 'success', 'message': 'Account created'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)