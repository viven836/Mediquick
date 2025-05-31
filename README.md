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

## 🛠️ How to Run Locally
Follow these steps to get the MediQuick prototype running on your machine:

### 🔧 Prerequisites
- Python 3.x
- MySQL installed and running
- Git
- A web browser (for the frontend)

### 📁 1. Clone the Repository
```
git clone https://github.com/your-username/mediquick.git
cd mediquick
```
---

### 🗃️ 2. Set Up the MySQL Database
Open your MySQL CLI.

Create the database:
```
CREATE DATABASE mediquick;
```
Import the schema and dummy data:
```
USE mediquick;
SOURCE path/to/your/schema_and_data.sql
```
Make sure the .sql file path is correct and inside your project.
---
### 🐍 3. Set Up the Backend (Flask)
```
cd backend
python -m venv venv
```
### Activate the virtual environment:
Windows:
```
.\venv\Scripts\activate
```
macOS/Linux:
```
source venv/bin/activate
```
Then install dependencies:
```
pip install -r requirements.txt
```
---
### ⚙️ 4. Configure Database Credentials
Update backend/db.py file with your MySQL details:
```
mysql_host = 'localhost'
mysql_user = 'your-username'
mysql_password = 'your-password'
mysql_db = 'mediquick'
```
---
### 🚀 5. Run the Backend Server
```
python app.py
```
Your Flask server should now be running at http://127.0.0.1:5000