from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with the API URL you want to call
API_URL = 'https://api.example.com/data'

@app.route('/')
def home():
    return "Welcome to the API server!"

@app.route('/call-api', methods=['GET'])
def call_api():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
