from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from extensions import db
from models.user_model import User

import bcrypt

# Blueprint
auth = Blueprint('auth', __name__)

# =========================
# REGISTER
# =========================

@auth.route('/register', methods=['POST'])
def register():

    try:

        data = request.get_json()

        if not data:
            return {
                "success": False,
                "message": "No data provided"
            }, 400

        email = data.get('email')
        password = data.get('password')

        # Validation
        if not email or not password:
            return {
                "success": False,
                "message": "Email and password are required"
            }, 400

        # Password validation
        if len(password) < 6:
            return {
                "success": False,
                "message": "Password must be at least 6 characters"
            }, 400

        # Check existing user
        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return {
                "success": False,
                "message": "User already exists"
            }, 409

        # Hash password
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        # Create user
        user = User(
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return {
            "success": True,
            "message": "User registered successfully"
        }, 201

    except Exception as e:

        db.session.rollback()

        return {
            "success": False,
            "error": str(e)
        }, 500


# =========================
# LOGIN
# =========================

@auth.route('/login', methods=['POST'])
def login():

    try:

        data = request.get_json()

        if not data:
            return {
                "success": False,
                "message": "No data provided"
            }, 400

        email = data.get('email')
        password = data.get('password')

        # Validation
        if not email or not password:
            return {
                "success": False,
                "message": "Email and password are required"
            }, 400

        # Find user
        user = User.query.filter_by(
            email=email
        ).first()

        # Invalid user
        if not user:
            return {
                "success": False,
                "message": "Invalid credentials"
            }, 401

        # Verify password
        password_correct = bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        )

        if not password_correct:
            return {
                "success": False,
                "message": "Invalid credentials"
            }, 401

        # Create JWT token
        token = create_access_token(
            identity=str(user.id)
        )

        return {
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email
            }
        }, 200

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }, 500