from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from model.model import *
from utils.auth_utility import role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    # Json data
    data = request.get_json(silent=True)
    username = data.get("username").strip() if data else None
    email = data.get("email").strip() if data else None
    phone = data.get("phone").strip() if data else None
    password = data.get("password").strip() if data else None
    role = data.get("role").strip() if data else None

    if not username or not email or not phone or not password or not role:
        response = {"message": "All fields are required."}

        return jsonify(response), 400

    user_email_exists = UserModel.query.filter_by(email=email).first()
    user_phone_exists = UserModel.query.filter_by(phone=phone).first()

    if user_email_exists or user_phone_exists:
        response = {"message": "User with this email or phone already exists."}
        return jsonify(response), 400

    if role == UserRole.ADMIN.value:
        response = {"message": "You cannot register as an admin."}
        return jsonify(response), 403  # forbidden error code

    try:

        # for trekker registration
        if role == UserRole.TREKKER.value:
            user = UserModel(
                username=username, email=email, phone=phone, role=UserRole.TREKKER.value
            )
            user.set_password(password)  # set password

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

        # for trekStaff registration
        elif role == UserRole.STAFF.value:

            user = UserModel(
                username=username, email=email, phone=phone, role=UserRole.STAFF.value
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            staff_profile = StaffModel(user_id=user.id)
            db.session.add(staff_profile)
            db.session.commit()

            response = {
                "message": "Staff registered successfully. Please wait for admin approval.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                },
                "staff_profile": {
                    "id": staff_profile.id,
                    "user_id": staff_profile.user_id,
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


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)
    email = data.get("email").strip() if data else None
    password = data.get("password").strip() if data else None
    role = data.get("role").strip() if data else None

    print(data)  # Debugging line to print the received data

    if not email or not password or not role:
        response = {"message": "Email, password, and role are required fields."}

        return jsonify(response), 400

    user = UserModel.query.filter_by(email=email).first()

    # Check if the user exists and if the password or role incorrect
    if not user or not user.check_password(password) or user.role != role:
        response = {"message": "Invalid email or password or role."}

        return jsonify(response), 401  # unauthorized error code

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


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # Invalidate the JWT token using Redis/DB [Later]

    response = {"message": "Logout successful."}
    return jsonify(response), 200

# to veriy the JWT token is valied
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
