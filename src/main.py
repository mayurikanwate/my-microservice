import os
import boto3
import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# AWS Secrets Manager Config
SECRET_NAME = "weather-api-key"
REGION_NAME = "us-east-1"  # Change this to your AWS region

def get_secret():
    """Fetch the API key from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=REGION_NAME)

    try:
        response = client.get_secret_value(SecretId=SECRET_NAME)
        secret = json.loads(response["SecretString"])
        return secret["OPENWEATHER_API_KEY"]
    except Exception as e:
        print(f"Error fetching secret: {e}")
        return None

# Fetch API key from AWS Secrets Manager
API_KEY = get_secret()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Weather Microservice!"})

@app.route('/weather/<city>')
def get_weather(city):
    if not API_KEY:
        return jsonify({"error": "API Key is missing!"}), 500

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"]
        })
    else:
        return jsonify({"error": "City not found!"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
