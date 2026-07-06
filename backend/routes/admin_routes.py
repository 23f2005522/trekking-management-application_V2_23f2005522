from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from utils.auth_utility import role_required
from model.model import *

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


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
                    .limit(6)
                    .all()
                )
            )
            fresh_bookings_JSON = [
                {
                    "id": booking.id,
                    "booking_date": booking.booking_date.strftime("%d %b %Y"),
                    "status": booking.status.value,
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
        data = request.get_json(silent=True)
        name = data.get("name") if data else None
        location = data.get("location") if data else None
        difficulty = data.get("difficulty") if data else None
        duration = data.get("duration") if data else None
        totalSlots = data.get("totalSlots") if data else None
        price = data.get("price") if data else None
        imageUrl = data.get("imageUrl") if data else None
        description = data.get("description") if data else None
        startDate = data.get("startDate") if data else None
        endDate = data.get("endDate") if data else None
        assignedStaffId = data.get("assignedStaffId") if data else None
        status = TrekStatus.TrekStatus.APPROVED if data.get("status") == TrekStatus.TrekStatus.APPROVED.value else TrekStatus.TrekStatus.PENDING


        # same trek cant be added before the previous trek is completed
        exsiting_trek = TrekModel.query.filter_by(name=name).first()
        if exsiting_trek:
            response = {
                "message": "A trek with the same name already exists. Please wait for the previous trek to be completed before adding a new one.",
            }
            return jsonify(response), 400

        # check even that assigned staff exists
        if assignedStaffId:
            staff_member = StaffModel.query.filter_by(
                id=assignedStaffId, role=UserRole.STAFF
            ).first()
            if not staff_member:
                response = {
                    "message": "The assigned staff member does not exist.",
                }
                return jsonify(response), 400

        new_trek = TrekModel(
            name=name,
            location=location,
            difficulty=TrekDifficulty(difficulty),
            duration=int(duration),
            total_slots=int(totalSlots),
            available_slots=int(totalSlots),
            price=float(price),
            image_url=imageUrl,
            description=description,
            starting_at=datetime.strptime(startDate, "%Y-%m-%d"),
            ending_at=datetime.strptime(endDate, "%Y-%m-%d"),
            assigned_staff_id=int(assignedStaffId) if assignedStaffId else None,
            status=status
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

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an error
        print(f"Error occurred while adding the trek: {e}")
        response = {
            "message": "An error occurred while adding the trek.",
        }
        return jsonify(response), 500


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
            trek.starting_at = datetime.strptime(
                data.get("startDate", trek.starting_at.strftime("%Y-%m-%d")), "%Y-%m-%d"
            )
            trek.ending_at = datetime.strptime(
                data.get("endDate", trek.ending_at.strftime("%Y-%m-%d")), "%Y-%m-%d"
            )
            
            trek.status = TrekStatus.APPROVED if data.get("status", trek.status.value) == TrekStatus.APPROVED.value else TrekStatus.PENDING

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

        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while updating the trek: {e}")
            response = {
                "message": "An error occurred while updating the trek.",
            }
            return jsonify(response), 500


# ManageStaff routes


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
        else:
            response = {
                "message": "Invalid action. Use 'blacklist' or 'deblacklist'.",
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
                "booking_cancel_reason": booking.booking_cancel_reason,
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
