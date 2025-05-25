'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# Load your model and vectorizer
model = joblib.load("emergency_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    symptoms = data.get("symptoms", "")

    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    vector = vectorizer.transform([symptoms])
    prediction = model.predict(vector)[0]

    return jsonify({
        "emergency": bool(prediction),
        "message": "🚨 Emergency detected!" if prediction else "✅ Not an emergency."
    })

if __name__ == "__main__":
    app.run(debug=True)'''

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')  # Pointing to your frontend folder
CORS(app)

# Load your ML model and vectorizer
model = joblib.load("emergency_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# 🏠 Homepage Route
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# 🧠 ML Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    symptoms = data.get("symptoms", "")
    
    if not symptoms.strip():
        return jsonify({"error": "No symptoms provided"}), 400

    vector = vectorizer.transform([symptoms])
    prediction = model.predict(vector)[0]

    return jsonify({
        "emergency": bool(prediction),
        "message": "🚨 Emergency detected!" if prediction else "✅ Not an emergency."
    })

if __name__ == '__main__':
    app.run(debug=True)

