
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import os
from db import get_db_connection
import math
from datetime import datetime

app = Flask(__name__, static_folder='../frontend', static_url_path='')  # Pointing to your frontend folder
CORS(app)

# Load both models
emergency_model = joblib.load("emergency_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
category_model = joblib.load("category_classifier.pkl")

# 🏠 Homepage Route
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        symptoms = data.get("symptoms", "")

        if not symptoms.strip():
            return jsonify({"error": "No symptoms provided"}), 400

        # Emergency prediction (works fine)
        vec_input = vectorizer.transform([symptoms])
        is_emergency = emergency_model.predict(vec_input)[0]

        # Category prediction (could be crashing)
        category = category_model.predict([symptoms])[0]

        return jsonify({
            "emergency": bool(is_emergency),
            "category": category,
            "message": "🚨 Emergency detected!" if is_emergency else "✅ Not an emergency."
        })

    except Exception as e:
        print("🔥 FLASK ERROR:", str(e))  # <-- Show full error in terminal
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route("/some-route")
def something():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM hospitals")
    results = cursor.fetchall()

    conn.close()
    return jsonify(results)
category_to_specialist = {
    "Cardiac": "Cardiologist",
    "Orthopedic": "Orthopedic Surgeon",
    "Allergic": "Allergist",
    "Neurological": "Neurologist",
    "Burns": "Burn Specialist",
    "Gastrointestinal": "Gastroenterologist",
    "Respiratory": "Pulmonologist",
    "Poisoning": "Toxicologist",
    "Skin Issues": "Dermatologist",
    "Mental Health": "Psychiatrist",
    "Pediatrics": "Pediatrician",
    "General": "General Physician",
    "Infectious": "Infectious Disease Specialist",
    "Preventive": "General Physician",
    "Routine Checkup": "General Physician",
    "Mild Symptoms": "General Physician"
}

def haversine(lat1, lon1, lat2, lon2):
    # Distance in km between two geo coords
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route("/book-bed", methods=["POST"])
def book_bed():
    try:
        data = request.get_json()
        name = data.get("name")
        phone = data.get("phone")
        lat = float(data.get("latitude"))
        lon = float(data.get("longitude"))
        category = data.get("category")
        specialist = category_to_specialist.get(category, "General Physician")  # fallback if undefined
  # This comes from the ML model

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Step 1: Find all hospitals with available beds and matching doctor
        try:
            cursor.execute("""
                SELECT h.id AS hospital_id, h.name, h.location_lat, h.location_lon
                FROM hospitals h
                JOIN beds b ON h.id = b.hospital_id
                JOIN doctors d ON h.id = d.hospital_id
                WHERE b.is_occupied = FALSE AND d.specialization = %s
                GROUP BY h.id
            """, (specialist,))
            
            hospitals = cursor.fetchall()
            print("Checking for hospitals with specialist:", specialist)
            print("Received lat/lon:", lat, lon)
            print("Hospitals found:", hospitals)

            if not hospitals:
                print("✅ Query ran, but no hospitals found with free beds and matching specialist.")
                return jsonify({"error": "No hospitals available with free beds and matching doctor."}), 404

        except Exception as db_error:
            print("🔥 SQL QUERY ERROR:", str(db_error))
            return jsonify({"error": "Database query failed", "details": str(db_error)}), 500


        # Step 2: Sort by distance
        for h in hospitals:
            h['distance'] = haversine(lat, lon, h['location_lat'], h['location_lon'])
        hospitals.sort(key=lambda x: x['distance'])

        selected_hospital = hospitals[0]

        # Step 3: Get a free bed in that hospital
        cursor.execute("""
            SELECT * FROM beds
            WHERE hospital_id = %s AND is_occupied = FALSE
            LIMIT 1
        """, (selected_hospital['hospital_id'],))
        bed = cursor.fetchone()

        if not bed:
            return jsonify({"error": "No free beds in selected hospital"}), 500

        # Step 4: Get a doctor with the required specialization
        cursor.execute("""
            SELECT * FROM doctors
            WHERE hospital_id = %s AND specialization = %s
            LIMIT 1
        """, (selected_hospital['hospital_id'], specialist))
        doctor = cursor.fetchone()

        # Step 5: Insert patient record
        cursor.execute("""
            INSERT INTO patients (name, phone, emergency_type, hospital_id, bed_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, phone, category, selected_hospital['hospital_id'], bed['id']))

        # Step 6: Mark bed as occupied
        cursor.execute("""
            UPDATE beds SET is_occupied = TRUE WHERE id = %s
        """, (bed['id'],))

        conn.commit()
        conn.close()

        return jsonify({
            "hospital": selected_hospital['name'],
            "bed_number": bed['bed_number'],
            "doctor": doctor['name'],
            "specialization": doctor['specialization'],
            "patient_name": name,
            "emergency_type": category
        })

    except Exception as e:
        print("🔥 Booking Error:", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route("/hospital-login", methods=["POST"])
def hospital_login():
    try:
        data = request.get_json()
        hospital_id = data.get("hospitalId")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id FROM hospitals
            WHERE id = %s AND password = %s
        """, (hospital_id, password))

        result = cursor.fetchone()
        conn.close()

        if result:
            return jsonify({"success": True, "hospitalId": hospital_id})
        else:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401

    except Exception as e:
        print("🔥 LOGIN ERROR:", str(e))
        return jsonify({"success": False, "error": "Server error"}), 500


@app.route("/hospital-patients/<int:hospital_id>", methods=["GET"])
def get_hospital_patients(hospital_id):
    try:
        category_to_specialist = {
            "Cardiac": "Cardiologist",
            "Orthopedic": "Orthopedic",
            "Allergic": "Allergist",
            "Neurological": "Neurologist",
            "Burns": "Burn Specialist",
            "Gastrointestinal": "Gastroenterologist",
            "Respiratory": "Pulmonologist",
            "Poisoning": "Toxicologist",
            "Skin Issues": "Dermatologist",
            "Mental Health": "Psychiatrist",
            "Pediatrics": "Pediatrician",
            "General": "General Physician",
            "Infectious": "Infectious Disease Specialist",
            "Preventive": "General Physician",
            "Routine Checkup": "General Physician",
            "Mild Symptoms": "General Physician"
        }

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT name FROM hospitals WHERE id = %s", (hospital_id,))
        hospital_info = cursor.fetchone()
        hospital_name = hospital_info["name"] if hospital_info else f"Hospital {hospital_id}"

        cursor.execute("""
            SELECT
                p.id as id,
                p.name AS patient_name,
                p.phone,
                p.emergency_type,
                p.timestamp,
                b.bed_number,
                p.hospital_id
            FROM patients p
            JOIN beds b ON p.bed_id = b.id
            WHERE p.hospital_id = %s
            ORDER BY p.timestamp DESC
        """, (hospital_id,))

        patients = cursor.fetchall()

        # 🔁 Add doctor info using mapping
        for p in patients:
            specialization = category_to_specialist.get(p["emergency_type"], "General Physician")

            cursor.execute("""
                SELECT name, specialization
                FROM doctors
                WHERE hospital_id = %s AND specialization = %s
                LIMIT 1
            """, (hospital_id, specialization))

            doctor = cursor.fetchone()

            if doctor:
                p["doctor_name"] = doctor["name"]
                p["specialization"] = doctor["specialization"]
            else:
                p["doctor_name"] = "N/A"
                p["specialization"] = specialization

        conn.close()
        return jsonify({
            "hospital_name": hospital_name,
            "patients": patients
        })

    except Exception as e:
        print("🔥 ERROR in /hospital-patients:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/discharge-patient", methods=["POST"])
def discharge_patient():
    try:
        data = request.get_json()
        patient_id = data.get("patientId")  # unique enough for now
        hospital_id = data.get("hospitalId")

        print(f"📥 Discharge requested for patient_id: {patient_id}, hospital_id: {hospital_id}")


        conn = get_db_connection()
        cursor = conn.cursor()

        # Step 1: Get bed ID before deleting
        cursor.execute("""
            SELECT bed_id FROM patients
            WHERE id = %s AND hospital_id = %s
            ORDER BY timestamp DESC
            LIMIT 1
        """, (patient_id, hospital_id))
        bed_result = cursor.fetchone()
        print("🛏️ Bed lookup result:", bed_result)

        if not bed_result:
            return jsonify({"success": False, "error": "Patient not found"}), 404

        bed_id = bed_result[0]
        print("✅ Bed ID associated:", bed_id)

        # Step 2: Delete patient record (soft delete alternative = add discharged column)
        cursor.execute("""
            DELETE FROM patients
            WHERE id = %s AND hospital_id = %s
        """, (patient_id, hospital_id))
        print("🗑️ Patient record deleted.")

        # Step 3: Free up the bed
        cursor.execute("""
            UPDATE beds SET is_occupied = FALSE WHERE id = %s
        """, (bed_id,))
        print("🛏️ Bed marked as free.")

        conn.commit()
        conn.close()

        print("✅ Discharge completed.")
        return jsonify({"success": True})

    except Exception as e:
        print("🔥 DISCHARGE ERROR:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


