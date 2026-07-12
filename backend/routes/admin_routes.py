from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from utils.auth_utility import role_required
from model.model import *

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


# load admin dashboard stats and recent bookings/treks
@admin_bp.route("/data", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_admin_data():
    if request.method == "GET":
        try:
            # fetch adminUser
            admin_user = UserModel.query.filter_by(role=UserRole.ADMIN).first()

            # fetch Dashboard stats
            total_trekkers = UserModel.query.filter_by(role=UserRole.TREKKER).count()
            total_staff = UserModel.query.filter_by(role=UserRole.STAFF).count()
            total_bookings = BookingModel.query.count()
            total_treks = TrekModel.query.count()
            total_revenue_till_data = (
                db.session.query(func.sum(BookingModel.amount_paid)).scalar() or 0
            )
            treks_approved = TrekModel.query.filter(
                TrekModel.status == TrekStatus.APPROVED
            ).count()
            treks_pending = TrekModel.query.filter(
                TrekModel.status == TrekStatus.PENDING
            ).count()

            # some recent bookings for the dashboard in JSON format
            fresh_bookings = list(
                (
                    BookingModel.query.order_by(BookingModel.booking_date.desc())
                    .limit(3)
                    .all()
                )
            )
            fresh_bookings_JSON = [
                {
                    "id": booking.id,
                    "booking_date": booking.booking_date.strftime("%d %b %Y"),
                    "booking_status": booking.status.value,
                    "amount_paid": booking.amount_paid,
                    "payment_status": booking.payment_status.value,
                    "user": {
                        "id": booking.user.id,
                        "username": booking.user.username,
                    },
                    "trek": {
                        "id": booking.trek.id,
                        "name": booking.trek.name,
                    },
                }
                for booking in fresh_bookings
            ]

            # some recent treks for the dashboard in JSON format
            fresh_treks = (
                TrekModel.query.order_by(TrekModel.created_at.desc()).limit(6).all()
            )
            fresh_treks_JSON = [
                {
                    "id": trek.id,
                    "name": trek.name,
                    "difficulty": trek.difficulty.value,
                    "location": trek.location,
                    "status": trek.status.value,
                    "assigned_staff_id": trek.staff.id if trek.staff else None,
                }
                for trek in fresh_treks
            ]

            # response data
            response = {
                "message": "Admin data fetched successfully.",
                "admin_user": {
                    "id": admin_user.id,
                    "username": admin_user.username,
                    "email": admin_user.email,
                    "phone": admin_user.phone,
                    "role": admin_user.role,
                },
                "dashboard_stats": {
                    "total_trekkers": total_trekkers,
                    "total_staff": total_staff,
                    "total_bookings": total_bookings,
                    "total_treks": total_treks,
                    "treks_approved": treks_approved,
                    "treks_pending": treks_pending,
                    "total_revenue_till_data": total_revenue_till_data,
                    "recent_bookings": fresh_bookings_JSON,
                    "recent_treks": fresh_treks_JSON,
                },
            }

            return jsonify(response), 200

        except Exception as e:
            print(f"Error fetching admin data: {str(e)}")
            response = {
                "message": "An error occurred while fetching admin data.",
            }
            return jsonify(response), 500


# trek management routes


# get all treks details
@admin_bp.route("/treks", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_treks():
    try:
        treks = TrekModel.query.all()
        treks_JSON = [
            {
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty.value,
                "TotalSlots": trek.total_slots,
                "availableSlots": trek.available_slots,
                "status": trek.status.value,
                "assigned_staff_id": (
                    trek.assigned_staff_id if trek.assigned_staff_id else None
                ),
            }
            for trek in treks
        ]

        response = {
            "message": "Treks fetched successfully.",
            "treks": treks_JSON,
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error fetching treks: {str(e)}")
        response = {
            "message": "An error occurred while fetching treks.",
        }
        return jsonify(response), 500


# add an new trek
@admin_bp.route("/addtrek", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def add_trek():
    try:
        data = request.get_json(silent=True) or {}

        name = data.get("name")
        location = data.get("location")
        difficulty = data.get("difficulty")
        duration = data.get("duration")
        totalSlots = data.get("totalSlots")
        price = data.get("price")
        imageUrl = data.get("imageUrl")
        description = data.get("description")
        startDate = data.get("startDate")
        endDate = data.get("endDate")
        assignedStaffId = data.get("assignedStaffId")
       
        if assignedStaffId == "" or assignedStaffId is None:
            response = {
                "message": "Assigned staff ID is required.",
            }
            return jsonify(response), 400
            
        status = (
            TrekStatus.APPROVED
            if data.get("status") == TrekStatus.APPROVED.value
            else TrekStatus.PENDING
        )

        # same trek cant be added before the previous trek is completed
        exsiting_trek = TrekModel.query.filter_by(name=name).first()
        if exsiting_trek:
            response = {
                "message": "A trek with the same name already exists. Please wait for the previous trek to be completed before adding a new one.",
            }
            return jsonify(response), 400

        # Now this safely checks if it's an actual value or ID
        if assignedStaffId is not None:
            staff_member = StaffModel.query.filter_by(id=int(assignedStaffId)).first()
            if not staff_member:
                response = {
                    "message": "The assigned staff member does not exist.",
                }
                return jsonify(response), 400
            if staff_member.Profile_status != StaffStatus.APPROVED:
                response = {
                    "message": "Only approved staff can be assigned to treks.",
                }
                return jsonify(response), 400

        # if duration not mathcing with start and end date
        if startDate and endDate and duration:
            start_date_obj = datetime.strptime(startDate, "%Y-%m-%d")
            end_date_obj = datetime.strptime(endDate, "%Y-%m-%d")

            if end_date_obj <= start_date_obj:
                response = {
                    "message": "Ending date must be after the starting date.",
                }
                return jsonify(response), 400

            calculated_duration = (end_date_obj - start_date_obj).days + 1

            if calculated_duration != int(duration):
                response = {
                    "message": "The provided duration does not match the difference between the start and end dates.",
                }
                return jsonify(response), 400

        new_trek = TrekModel(
            name=name,
            location=location,
            difficulty=TrekDifficulty(difficulty),
            duration=int(duration),
            total_slots=int(totalSlots) if totalSlots is not None else 0,
            available_slots=int(totalSlots) if totalSlots is not None else 0,
            price=float(price),
            image_url=imageUrl,
            description=description,
            starting_at=datetime.strptime(startDate, "%Y-%m-%d"),
            ending_at=datetime.strptime(endDate, "%Y-%m-%d"),
            assigned_staff_id=int(assignedStaffId),
            status=status,
        )

        db.session.add(new_trek)
        db.session.commit()

        response = {
            "message": "Trek added successfully.",
            "trek": {
                "id": new_trek.id,
                "name": new_trek.name,
                "location": new_trek.location,
                "difficulty": new_trek.difficulty.value,
                "total_slots": new_trek.total_slots,
                "available_slots": new_trek.available_slots,
                "price": new_trek.price,
                "image_url": new_trek.image_url,
                "description": new_trek.description,
                "starting_at": new_trek.starting_at.strftime("%Y-%m-%d"),
                "ending_at": new_trek.ending_at.strftime("%Y-%m-%d"),
                "assigned_staff_id": new_trek.assigned_staff_id,
            },
        }

        return jsonify(response), 201

    except IntegrityError as e:
        db.session.rollback()
        print(f"Error occurred while adding the trek: {e}")
        if "ending before start" in str(e).lower():
            message = "Ending date must be after the starting date."
        else:
            message = "Invalid trek data. Please check your inputs."
        return jsonify({"message": message}), 400

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an error
        print(f"Error occurred while adding the trek: {e}")
        response = {
            "message": "An error occurred while adding the trek.",
        }
        return jsonify(response), 500


# get trek details for edit form or save updated trek info
@admin_bp.route("/edittrek/<int:trek_id>", methods=["GET", "POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def edit_trek(trek_id):

    if request.method == "GET":
        try:
            trek = TrekModel.query.get(trek_id)
            if not trek:
                response = {
                    "message": "Trek not found.",
                }
                return jsonify(response), 404

            trek_JSON = {
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty.value,
                "duration": trek.duration,
                "totalSlots": trek.total_slots,
                "availableSlots": trek.available_slots,
                "price": trek.price,
                "imageUrl": trek.image_url,
                "description": trek.description,
                "startDate": trek.starting_at.strftime("%Y-%m-%d"),
                "endDate": trek.ending_at.strftime("%Y-%m-%d"),
                "assigned_staff_id": trek.assigned_staff_id,
                "status": trek.status.value,
            }

            response = {
                "message": "Trek fetched successfully.",
                "trek": trek_JSON,
            }

            return jsonify(response), 200

        except Exception as e:
            print(f"Error fetching trek: {str(e)}")
            response = {
                "message": "An error occurred while fetching the trek.",
            }
            return jsonify(response), 500

    if request.method == "POST":

        trek = TrekModel.query.filter(TrekModel.id == int(trek_id)).first()

        if not trek:
            response = {
                "message": "Trek not found.",
            }
            return jsonify(response), 404

        ## Update trek details
        try:

            data = request.get_json(silent=True)
            print(f"Received data for updating trek: {data}")

            # check even that assigned staff exists
            assigned_staff_id = data.get("assigned_staff_id", 9999999)
            print(f"Received assigned_staff_id: {assigned_staff_id}")
            if assigned_staff_id:
                staff_member = StaffModel.query.filter_by(
                    id=int(assigned_staff_id)
                ).first()
                if not staff_member:
                    response = {
                        "message": "The assigned staff member does not exist.",
                    }
                    return jsonify(response), 400
                if staff_member.Profile_status != StaffStatus.APPROVED:
                    response = {
                        "message": "Only approved staff can be assigned to treks.",
                    }
                    return jsonify(response), 400

            trek.assigned_staff_id = (
                int(assigned_staff_id) if assigned_staff_id else None
            )

            trek.name = data.get("name", trek.name)
            trek.location = data.get("location", trek.location)
            trek.difficulty = TrekDifficulty(
                data.get("difficulty", trek.difficulty.value)
            )
            trek.duration = int(data.get("duration", trek.duration))
            trek.total_slots = int(data.get("totalSlots", trek.total_slots))
            trek.available_slots = int(data.get("availableSlots", trek.available_slots))
            trek.price = float(data.get("price", trek.price))
            trek.image_url = data.get("imageUrl", trek.image_url)
            trek.description = data.get("description", trek.description)

            start_date_str = data.get("startDate", trek.starting_at.strftime("%Y-%m-%d"))
            end_date_str = data.get("endDate", trek.ending_at.strftime("%Y-%m-%d"))
            start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d")

            if end_date_obj <= start_date_obj:
                response = {
                    "message": "Ending date must be after the starting date.",
                }
                return jsonify(response), 400

            duration_value = int(data.get("duration", trek.duration))
            calculated_duration = (end_date_obj - start_date_obj).days + 1
            if calculated_duration != duration_value:
                response = {
                    "message": "The provided duration does not match the difference between the start and end dates.",
                }
                return jsonify(response), 400

            available_slots = int(data.get("availableSlots", trek.available_slots))
            total_slots = int(data.get("totalSlots", trek.total_slots))
            if available_slots > total_slots:
                response = {
                    "message": "Available slots cannot be greater than total slots.",
                }
                return jsonify(response), 400

            trek.starting_at = start_date_obj
            trek.ending_at = end_date_obj

            status_value = data.get("status", trek.status.value)
            try:
                trek.status = TrekStatus(status_value)
            except ValueError:
                trek.status = TrekStatus.PENDING

            db.session.commit()
            response = {
                "message": "Trek updated successfully.",
                "trek": {
                    "id": trek.id,
                    "name": trek.name,
                    "location": trek.location,
                    "difficulty": trek.difficulty.value,
                    "total_slots": trek.total_slots,
                    "available_slots": trek.available_slots,
                    "price": trek.price,
                    "image_url": trek.image_url,
                    "description": trek.description,
                    "starting_at": trek.starting_at.strftime("%Y-%m-%d"),
                    "ending_at": trek.ending_at.strftime("%Y-%m-%d"),
                    "assigned_staff_id": trek.assigned_staff_id,
                    "status": trek.status.value,
                },
            }
            return jsonify(response), 200

        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred while updating the trek: {e}")
            if "ending before start" in str(e).lower():
                message = "Ending date must be after the starting date."
            else:
                message = "Invalid trek data. Please check your inputs."
            return jsonify({"message": message}), 400

        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while updating the trek: {e}")
            response = {
                "message": "An error occurred while updating the trek.",
            }
            return jsonify(response), 500


# delete a trek when admin no longer needs it
@admin_bp.route("/deletetrek/<int:trek_id>", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def delete_trek(trek_id):
    try:
        trek = TrekModel.query.get(trek_id)
        if not trek:
            return jsonify({"message": "Trek not found."}), 404

        trek_name = trek.name
        db.session.delete(trek)
        db.session.commit()

        return jsonify(
            {
                "message": f"Trek '{trek_name}' deleted successfully.",
                "trek_id": trek_id,
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while deleting the trek: {e}")
        return jsonify({"message": "An error occurred while deleting the trek."}), 500


# ManageStaff routes


# admin creates a new staff account (starts as pending)
@admin_bp.route("/create_staff", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def create_staff():
    try:
        data = request.get_json(silent=True) or {}

        username = (data.get("username") or "").strip()
        email = (data.get("email") or "").strip()
        phone = (data.get("phone") or "").strip()
        password = (data.get("password") or "").strip()
        experience = data.get("experience", 0)
        address = (data.get("address") or "").strip() or None
        contact_number = (data.get("contact_number") or "").strip() or None
        staff_bio = (data.get("staff_bio") or "").strip() or None

        if not username or not email or not phone or not password:
            return jsonify({"message": "Username, email, phone, and password are required."}), 400

        if UserModel.query.filter_by(email=email).first():
            return jsonify({"message": "A user with this email already exists."}), 400

        if UserModel.query.filter_by(phone=phone).first():
            return jsonify({"message": "A user with this phone number already exists."}), 400

        user = UserModel(
            username=username,
            email=email,
            phone=phone,
            role=UserRole.STAFF.value,
            is_active=False,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        staff_profile = StaffModel(
            user_id=user.id,
            experience=int(experience) if experience is not None else 0,
            address=address,
            contact_number=contact_number,
            staff_bio=staff_bio,
            Profile_status=StaffStatus.PENDING,
        )
        db.session.add(staff_profile)
        db.session.commit()

        return jsonify(
            {
                "message": "Staff account created successfully. Approve the account before they can log in.",
                "staff": {
                    "user_id": user.id,
                    "staff_id": staff_profile.id,
                    "username": user.username,
                    "phone": user.phone,
                    "email": user.email,
                    "status": staff_profile.Profile_status.value,
                    "is_active": user.is_active,
                },
            }
        ), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while creating staff member: {e}")
        return jsonify({"message": "An error occurred while creating the staff member."}), 500


# get all staff members
@admin_bp.route("/staffs", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_staffs():

    try:
        user_staff = UserModel.query.filter_by(role=UserRole.STAFF).all()

        staffs_JSON = [
            {
                "user_id": user.id,
                "staff_id": user.staff_profile.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "status": user.staff_profile.Profile_status.value,
                "is_active": user.is_active,
                "blacklisted_reason": user.blacklisted_reason,
            }
            for user in user_staff
        ]
        return jsonify({"staffs": staffs_JSON}), 200

    except Exception as e:
        print(f"Error occurred while fetching staff members: {e}")

        response = {
            "message": "An error occurred while fetching staff members.",
        }
        return jsonify(response), 500


# Approve or Reject or Blacklist or dePending staff member
@admin_bp.route("/staffs/<int:staff_id>/<string:status>", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def update_staff_status(staff_id, status):
    try:
        staff_user = UserModel.query.filter_by(id=staff_id, role=UserRole.STAFF).first()
        if not staff_user:
            response = {
                "message": "Staff member not found.",
            }
            return jsonify(response), 404

        data = request.get_json(silent=True)
        reason = (
            data.get("reason") if data and data.get("reason") else "No reason provided"
        )

        if status.lower() == StaffStatus.APPROVED.value.lower():
            staff_user.is_blacklisted = False
            staff_user.staff_profile.Profile_status = StaffStatus.APPROVED
            staff_user.is_active = True
            staff_user.blacklisted_reason = None

        elif status.lower() == StaffStatus.REJECTED.value.lower():
            staff_user.staff_profile.Profile_status = StaffStatus.REJECTED
            staff_user.is_active = False
            staff_user.blacklisted_reason = reason

        elif status.lower() == StaffStatus.BLACKLISTED.value.lower():
            staff_user.is_blacklisted = True
            staff_user.staff_profile.Profile_status = StaffStatus.BLACKLISTED
            staff_user.is_active = False
            staff_user.blacklisted_reason = reason

        elif status.lower() == StaffStatus.PENDING.value.lower():
            staff_user.staff_profile.Profile_status = StaffStatus.PENDING
            staff_user.is_active = False
            staff_user.blacklisted_reason = None

        else:
            response = {
                "message": "Invalid status. Use 'approved', 'rejected', 'blacklisted', or 'pending'.",
            }
            return jsonify(response), 400

        db.session.commit()

        response = {
            "message": f"Staff member {status} successfully.",
            "staff": {
                "user_id": staff_user.id,
                "username": staff_user.username,
                "phone": staff_user.phone,
                "email": staff_user.email,
                "status": staff_user.staff_profile.Profile_status.value,
                "is_active": staff_user.is_active,
                "blacklisted_reason": staff_user.blacklisted_reason,
            },
        }

        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while updating staff status: {e}")
        response = {
            "message": "An error occurred while updating staff status.",
        }
        return jsonify(response), 500


# Trekkers routes


# get all trekkers
@admin_bp.route("/trekkers", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_trekkers():

    try:
        user_trekkers = UserModel.query.filter_by(role=UserRole.TREKKER).all()

        trekkers_JSON = [
            {
                "user_id": user.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "is_active": user.is_active,
                "is_blacklisted": user.is_blacklisted,
                "blacklisted_reason": user.blacklisted_reason,
            }
            for user in user_trekkers
        ]
        return jsonify({"trekkers": trekkers_JSON}), 200

    except Exception as e:
        print(f"Error occurred while fetching trekkers: {e}")

        response = {
            "message": "An error occurred while fetching trekkers.",
        }
        return jsonify(response), 500


# Blacklist or deBlacklist trekker
@admin_bp.route("/trekkers/<int:trekker_id>/<string:action>", methods=["POST"])
@jwt_required()
@role_required(UserRole.ADMIN)
def update_trekker_status(trekker_id, action):
    try:
        trekker_user = UserModel.query.filter_by(
            id=trekker_id, role=UserRole.TREKKER
        ).first()
        if not trekker_user:
            response = {
                "message": "Trekker not found.",
            }
            return jsonify(response), 404

        data = request.get_json(silent=True)
        reason = (
            data.get("reason") if data and data.get("reason") else "No reason provided"
        )

        if action.lower() == "blacklist":
            trekker_user.is_blacklisted = True
            trekker_user.is_active = False
            trekker_user.blacklisted_reason = reason
        elif action.lower() == "deblacklist":
            trekker_user.is_blacklisted = False
            trekker_user.is_active = True
            trekker_user.blacklisted_reason = None
        elif action.lower() == "deactivate":
            if trekker_user.is_blacklisted:
                response = {
                    "message": "Cannot deactivate a blacklisted trekker. Remove blacklist first.",
                }
                return jsonify(response), 400
            trekker_user.is_active = False
        elif action.lower() == "reactivate":
            if trekker_user.is_blacklisted:
                response = {
                    "message": "Cannot reactivate a blacklisted trekker. Remove blacklist first.",
                }
                return jsonify(response), 400
            trekker_user.is_active = True
        else:
            response = {
                "message": "Invalid action. Use 'blacklist', 'deblacklist', 'deactivate', or 'reactivate'.",
            }
            return jsonify(response), 400

        db.session.commit()

        response = {
            "message": f"Trekker {action}ed successfully.",
            "trekker": {
                "user_id": trekker_user.id,
                "username": trekker_user.username,
                "phone": trekker_user.phone,
                "email": trekker_user.email,
                "is_active": trekker_user.is_active,
                "is_blacklisted": trekker_user.is_blacklisted,
                "blacklisted_reason": trekker_user.blacklisted_reason,
            },
        }

        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while updating trekker status: {e}")
        response = {
            "message": "An error occurred while updating trekker status.",
        }
        return jsonify(response), 500


# Booking routes


# get all bookings
@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def get_bookings():
    try:
        bookings = BookingModel.query.order_by(BookingModel.booking_date.desc()).all()

        bookings_JSON = [
            {
                "id": booking.id,
                "user_id": booking.user_id,
                "username": booking.user.username,
                "user_email": booking.user.email,
                "trek_id": booking.trek_id,
                "trek_name": booking.trek.name,
                "booking_date": booking.booking_date.strftime("%Y-%m-%d"),
                "status": booking.status.value,
                "payment_status": booking.payment_status.value,
                "amount_paid": float(booking.amount_paid),
                "booking_cancel_date": (
                    booking.booking_cancel_date.strftime("%Y-%m-%d")
                    if booking.booking_cancel_date
                    else None
                ),
            }
            for booking in bookings
        ]

        return (
            jsonify(
                {
                    "message": "Bookings fetched successfully.",
                    "bookings": bookings_JSON,
                }
            ),
            200,
        )

    except Exception as e:
        print(f"Error occurred while fetching bookings: {e}")
        response = {
            "message": "An error occurred while fetching bookings.",
        }
        return jsonify(response), 500


# report generation routes


# pull full admin report with trek/booking/revenue breakdown
@admin_bp.route("/report", methods=["GET"])
@jwt_required()
@role_required(UserRole.ADMIN)
def generate_report():
    # Overview
    total_trekkers = UserModel.query.filter_by(role=UserRole.TREKKER).count()
    total_staff = UserModel.query.filter_by(role=UserRole.STAFF).count()
    total_treks = TrekModel.query.count()
    total_bookings = BookingModel.query.count()

    # Trek Status

    open_count = TrekModel.query.filter_by(status=TrekStatus.OPEN).count()
    ongoing_count = TrekModel.query.filter_by(status=TrekStatus.ONGOING).count()
    completed_count = TrekModel.query.filter_by(status=TrekStatus.COMPLETED).count()
    pending_count = TrekModel.query.filter_by(status=TrekStatus.PENDING).count()
    approved_count = TrekModel.query.filter_by(status=TrekStatus.APPROVED).count()

    # Booking Status

    booked = BookingModel.query.filter_by(status=BookingStatus.BOOKED).count()
    completed = BookingModel.query.filter_by(status=BookingStatus.COMPLETED).count()
    cancelled = BookingModel.query.filter_by(status=BookingStatus.CANCELED).count()

    # Payment Statistics

    paid = BookingModel.query.filter_by(payment_status=PaymentStatus.PAID).count()
    pending = BookingModel.query.filter_by(payment_status=PaymentStatus.PENDING).count()
    revenue = db.session.query(db.func.sum(BookingModel.amount_paid)).scalar() or 0

    # popular treks based on the number of bookings
    popular_treks = (
        db.session.query(
            TrekModel.name,
            db.func.count(BookingModel.id).label("booking_count"),
        )
        .join(BookingModel, BookingModel.trek_id == TrekModel.id)
        .group_by(TrekModel.id)
        .order_by(db.desc("booking_count"))
        .limit(5)
        .all()
    )

    popular_treks_JSON = [
        {"trek_name": trek.name, "booking_count": trek.booking_count}
        for trek in popular_treks
    ]

    response = {
        "message": "Report generated successfully.",
        "overview": {
            "total_trekkers": total_trekkers,
            "total_staff": total_staff,
            "total_treks": total_treks,
            "total_bookings": total_bookings,
        },
        "trek_status": {
            "open": open_count,
            "ongoing": ongoing_count,
            "completed": completed_count,
            "pending": pending_count,
            "approved": approved_count,
        },
        "booking_status": {
            "booked": booked,
            "completed": completed,
            "cancelled": cancelled,
        },
        "payment_statistics": {
            "paid": paid,
            "pending": pending,
            "revenue": revenue,
        },
        "popular_treks": popular_treks_JSON,
    }

    return jsonify(response), 200
