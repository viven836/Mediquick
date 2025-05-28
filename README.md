# 🚑 MediQuick

> AI + IoT-based Emergency Hospital Bed Booking System
> Helping users get urgent care in seconds — not minutes.

## 🩺 What is MediQuick?

MediQuick is a web-based emergency triage system that uses **machine learning**, **geolocation**, and **hospital data** to:

- 🔍 Detect if a user is experiencing a **medical emergency**
- 🧠 Classify the **type of emergency** (e.g. Cardiac, Orthopedic, Allergic)
- 📍 Use **location + doctor + bed availability** to book a hospital bed in real time
- 🏥 Update the hospital's dashboard with patient info
- ⚙️ (Optional) Use an IoT-based bed occupancy sensor via Force Sensing Resistor (FSR)

## ⚙️ Tech Stack

| Layer | Tools / Frameworks |
|-------|-------------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Flask (Python) + Flask-CORS |
| Database | MySQL (patients, doctors, beds, hospitals) |
| Machine Learning | Logistic Regression (Emergency detection) + Text Classifier (Emergency category) |
| ML Deployment | joblib + Flask |
| Optional IoT | FSR Sensor (bed occupancy detection) |

## 💻 Features

- 🔠 **Text-based & questionnaire-based symptom input**
- 🤖 **AI emergency detection** (Emergency vs Non-Emergency)
- 📚 **Emergency category prediction** (Cardiac, Burns, Neurological, etc.)
- 🏥 **Location-based hospital selection**
- 🛏️ **Real-time bed booking**
- 👨‍⚕️ **Doctor specialization matching**
- 🧾 **Hospital dashboard with discharge option**
- 🌐 **Frontend-backend synced via REST API**
