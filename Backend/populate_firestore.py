from flask import Flask, jsonify
from config import Config
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Firebase
cred = credentials.Certificate('C:/Users/LENOVO/Desktop/House/Backend/house.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/api/departments', methods=['GET'])
def get_departments():
    departments = []

    # Retrieve department data from Firestore
    department_docs = db.collection('departments').get()

    for doc in department_docs:
        department = {
            'id': doc.id,
            'name': doc.get('name')
        }
        departments.append(department)

    return jsonify(departments)

@app.route('/api/departments/<department_id>/devices', methods=['GET'])
def get_devices(department_id):
    devices = []

    # Retrieve device data from Firestore based on the department_id
    device_docs = db.collection('departments').document(department_id).collection('devices').get()

    for doc in device_docs:
        device = {
            'id': doc.id,
            'name': doc.get('name'),
            'department_id': department_id
        }
        devices.append(device)

    return jsonify(devices)

if __name__ == '__main__':
    app.run()