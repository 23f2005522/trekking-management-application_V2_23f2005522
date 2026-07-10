from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from model.model import *

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# register a new trekker account (staff/admin cant sign up here)
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    password = (data.get("password") or "").strip()
    role = (data.get("role") or "trekker").strip()

    if not username or not email or not phone or not password:
        return jsonify({"message": "All fields are required."}), 400

    if role == UserRole.ADMIN.value:
        return jsonify({"message": "You cannot register as an admin."}), 403

    if role == UserRole.STAFF.value:
        return jsonify({
            "message": "Trek staff accounts are created by the administrator only."
        }), 403

    if role != UserRole.TREKKER.value:
        return jsonify({"message": "Invalid role. Only trekker registration is allowed."}), 400

    user_email_exists = UserModel.query.filter_by(email=email).first()
    user_phone_exists = UserModel.query.filter_by(phone=phone).first()

    if user_email_exists or user_phone_exists:
        return jsonify({"message": "User with this email or phone already exists."}), 400

    try:
        user = UserModel(
            username=username, email=email, phone=phone, role=UserRole.TREKKER.value
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        response = {
            "message": "User registered successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
            },
            "username": user.username,
            "role": user.role,
        }

        return jsonify(response), 201

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an error
        print(f"Error occurred while registering the user: {e}")
        response = {
            "message": "An error occurred while registering the user.",
        }
        return jsonify(response), 500


# login with email password and role, returns jwt token
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    role = (data.get("role") or "").strip()

    if not email or not password or not role:
        return jsonify({"message": "Email, password, and role are required fields."}), 400

    user = UserModel.query.filter_by(email=email).first()

    # Check if the user exists and if the password or role incorrect
    if not user or not user.check_password(password) or user.role != role:
        response = {"message": "Invalid email or password or role."}

        return jsonify(response), 401  # unauthorized error code

    if user.role == UserRole.TREKKER.value:
        if not user.is_active:
            response = {"message": "Account deactivated. Contact the administrator."}
            return jsonify(response), 403
        if user.is_blacklisted:
            response = {"message": "Account blacklisted. Contact the administrator."}
            return jsonify(response), 403

    # check if staff need approval or he was rejected by admin
    if user.role == UserRole.STAFF.value:
        if user.staff_profile.Profile_status == StaffStatus.PENDING.value:
            response = {"message": "Staff account needs approval."}
            return jsonify(response), 401
        if user.staff_profile.Profile_status == StaffStatus.REJECTED.value:
            response = {
                "message": "Staff account has been rejected by the administrator."
            }
            return jsonify(response), 403
        if user.staff_profile.Profile_status == StaffStatus.BLACKLISTED.value:
            response = {
                "message": "Staff account has been blacklisted by the administrator."
            }
            return jsonify(response), 403

    # Create a JWT token for the user
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "email": user.email},
    )

    response = {
        "message": "Login successful.",
        "access_token": access_token,
        "role": user.role,
        "username": user.username,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
        },
    }

    if user.role == UserRole.STAFF.value:
        response["staff_profile"] = {
            "id": user.staff_profile.id,
            "profile_status": user.staff_profile.Profile_status,
        }

    return jsonify(response), 200


# logout endpoint (frontend clears the token for now)
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # Invalidate the JWT token using Redis/DB [Later]

    response = {"message": "Logout successful."}
    return jsonify(response), 200


# quick check if the logged in jwt token is still valid
@auth_bp.route("/authme", methods=["GET"])
@jwt_required()
def verify():

    return jsonify({
        "authenticated": True
    }), 200

# for testing the role_required decorator and JWT token
# @auth_bp.route("/protected", methods=["GET"])
# @jwt_required()
# @role_required(UserRole.ADMIN.value)

# def protected():
#     tokendata = get_jwt ()  # getting the data from the JWT token
#     userid = tokendata.get("sub")  # getting the user id from the token data
#     user_emial = tokendata.get("email")  # getting the user email from the token data
#     user_role = tokendata.get("role")  # getting the user role from the token data

#     print(f"User ID: {userid}, Email: {user_emial}, Role: {user_role}")  # printing the user data to the console

#     response = {
#         "message": "You have accessed a protected route.",
#         "user_id": userid,
#         "user_email": user_emial,
#         "user_role": user_role,
#     }

#     return jsonify(response), 200
