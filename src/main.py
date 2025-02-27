import os
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the API key from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")
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
