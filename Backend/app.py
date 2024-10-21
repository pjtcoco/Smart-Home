from flask import Flask, request, jsonify, session
from firebase_admin import auth
from firebase_admin import credentials,firestore
from config import Config, app
import firebase_admin
from model import Department, Device

# Initialize Flask app

app.config.from_object(Config)

# Initialize Firebase
cred = credentials.Certificate('C:/Users/LENOVO/Desktop/House/Backend/house.json')
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Route for user signup
@app.route('/api/signup', methods=['POST'])
def signup():
    # Check if the user is already signed up
    if 'user_id' in session:
        return jsonify({'message': 'Already signed up'}), 200

    # Get user data from the request body
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    # Validate request data
    if not name or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Check if user with the given email already exists
        auth.get_user_by_email(email)

        # If user already exists, return an error message
        return jsonify({'error': 'Email already exists'}), 400

    except auth.UserNotFoundError:
        try:
            # Create a new user with email and password
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )

            # Customize additional user properties if needed
            # user.update_property('property_name', 'property_value')

            # Store the user ID in the session to indicate signup completion
            session['user_id'] = user.uid

            return jsonify({'message': 'User created successfully', 'user': user.uid}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500


# Route for user login
@app.route('/api/login', methods=['POST'])
def login():
    # Check if the user is already logged in
    if 'user_id' in session:
        return jsonify({'message': 'Already logged in'}), 200

    data = request.get_json()
    email = data['email']
    password = data['password']

    try:
        user = auth.get_user_by_email(email)  # Retrieve the user information

        # Implement your login logic here
        # Verify the user's credentials, generate tokens, etc.

        # Store the user ID in the session to indicate login completion
        session['user_id'] = user.uid

        return jsonify({'message': 'Login successful'})
    except auth.AuthError as e:
        return jsonify({'error': str(e)}), 400

# # API route for retrieving department information
# @app.route('/api/departments', methods=['GET'])
# def get_departments():
#     departments = Department.get_all()
#     return jsonify({'departments': departments})

@app.route('/api/departments', methods=['GET'])
def get_departments():
    departments = []
    
    # Fetch departments from Firestore
    collection_ref = db.collection('Departments')
    docs = collection_ref.stream()
    
    for doc in docs:
        department = doc.to_dict()
        departments.append(department)

    return jsonify(departments)

# API route for retrieving device information within a department
@app.route('/api/departments/<department_id>/devices', methods=['GET'])
def get_devices(department_id):
    devices = Device.get_by_department(department_id)
    return jsonify({'devices': devices})

# ... Additional API routes ...

# Retrieve and display users
def view_users():
    users = firebase_admin.auth.list_users()
    
    for user in users:
        user.to_dict()
        print(f"User ID: {user.uid}")
        print(f"Email: {user.email}")
        print(f"Display Name: {user.display_name}")
        print(f"Custom Claims: {user.custom_claims}")
        print("---")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='172.20.10.2', port=5000) 