from datetime import datetime
import os
import time

from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required

from config.config import Config
from utils.cache_utility import clear_trekker_open_treks_cache
from extensions.cache import cache
from model.model import *
from utils.auth_utility import role_required

trekker_bp = Blueprint("trekker_routes", __name__, url_prefix="/api/trekker")


# helper to shape trek data before sending to frontend
def trek_serializer(trek):
    return {
        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "difficulty": trek.difficulty.value if trek.difficulty else None,
        "duration": trek.duration,
        "total_slots": trek.total_slots,
        "available_slots": trek.available_slots,
        "price": float(trek.price),
        "image_url": trek.image_url,
        "starting_date": trek.starting_at.strftime("%Y-%m-%d"),
        "ending_date": trek.ending_at.strftime("%Y-%m-%d"),
        "status": trek.status.value if trek.status else None,
        "description": trek.description,
    }


# helper to shape booking data for lists and details
def booking_serializer(booking):
    return {
        "id": booking.id,
        "trek_id": booking.trek_id,
        "trek_name": booking.trek.name if booking.trek else None,
        "booking_date": (
            booking.booking_date.strftime("%Y-%m-%d") if booking.booking_date else None
        ),
        "status": booking.status.value if booking.status else None,
        "payment_status": (
            booking.payment_status.value if booking.payment_status else None
        ),
        "amount_paid": (
            float(booking.amount_paid) if booking.amount_paid is not None else 0.0
        ),
        "trek_status": (
            booking.trek.status.value if booking.trek and booking.trek.status else None
        ),
    }


# helper to shape trekker profile data
def user_serializer(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": user.role.value if user.role else None,
        "is_active": user.is_active,
        "is_blacklisted": user.is_blacklisted,
        "blacklisted_reason": user.blacklisted_reason,
    }


# load trekker dashboard with booking counts and recent stuff
@trekker_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@role_required(UserRole.TREKKER)
def get_trekker_dashboard():

    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404

    bookings = BookingModel.query.filter_by(user_id=user.id).all()

    active_bookings = [
        booking for booking in bookings if booking.status == BookingStatus.BOOKED
    ]

    completed_bookings = [
        booking for booking in bookings if booking.status == BookingStatus.COMPLETED
    ]

    canceled_bookings = [
        booking for booking in bookings if booking.status == BookingStatus.CANCELED
    ]

    recent_bookings = sorted(
        bookings,
        key=lambda booking: booking.booking_date,
        reverse=True,
    )[:5]

    recent_open_treks = (
        TrekModel.query.filter_by(status=TrekStatus.OPEN)
        .order_by(TrekModel.created_at.desc())
        .limit(5)
        .all()
    )

    recent_bookings_json = [booking_serializer(booking) for booking in recent_bookings]

    recent_open_treks_json = [trek_serializer(trek) for trek in recent_open_treks]

    return (
        jsonify(
            {
                "message": "Welcome to your dashboard!",
                "trekker_profile": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role.value,
                },
                "dashboard_stats": {
                    "total_bookings": len(bookings),
                    "active_bookings": len(active_bookings),
                    "completed_bookings": len(completed_bookings),
                    "canceled_bookings": len(canceled_bookings),
                },
                "recent_bookings": recent_bookings_json,
                "recent_open_treks": recent_open_treks_json,
            }
        ),
        200,
    )


# fetch or update trekker profile details
@trekker_bp.route("/profile", methods=["GET", "POST"])
@jwt_required()
@role_required(UserRole.TREKKER)
def get_trekker_profile():
    user_id = int(get_jwt_identity())
    print(f"Fetching profile for user_id: {user_id}")
    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404

    print(f"{user}")
    if request.method == "GET":
        return (
            jsonify(
                {
                    "message": "Trekker profile fetched successfully.",
                    "trekker_profile": user_serializer(user),
                }
            ),
            200,
        )

    if request.method == "POST":
        data = request.get_json(silent=True) or {}

        # the data tath come for update only update that data and keep the rest as it is

        username = data.get("username", user.username)
        email = data.get("email", user.email)
        phone = data.get("phone", user.phone)

        print(f"Received data for profile update: {data}")

        username = username.strip() if isinstance(username, str) else user.username
        email = email.strip() if isinstance(email, str) else user.email
        phone = phone.strip() if isinstance(phone, str) else user.phone

        if not username or not email or not phone:
            return jsonify({"message": "Username, email, and phone are required."}), 400

        email_exists = UserModel.query.filter(
            UserModel.email == email,
            UserModel.id != user.id,
        ).first()

        if email_exists:
            return jsonify({"message": "Email is already used by another user."}), 400

        phone_exists = UserModel.query.filter(
            UserModel.phone == phone,
            UserModel.id != user.id,
        ).first()

        if phone_exists:
            return jsonify({"message": "Phone is already used by another user."}), 400

        try:
            user.username = username
            user.email = email
            user.phone = phone
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while updating trekker profile: {e}")
            return (
                jsonify({"message": "An error occurred while updating profile."}),
                500,
            )

        return (
            jsonify(
                {
                    "message": "Trekker profile updated successfully.",
                    "trekker_profile": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "phone": user.phone,
                        "role": user.role.value,
                        "is_active": user.is_active,
                        "is_blacklisted": user.is_blacklisted,
                        "blacklisted_reason": user.blacklisted_reason,
                    },
                }
            ),
            200,
        )


# browse open treks with optional search and filters
@trekker_bp.route("/treks", methods=["GET"])
@jwt_required()
@role_required(UserRole.TREKKER)
@cache.cached(timeout=120, key_prefix=Config.TREKKER_OPEN_TREKS_KEY, query_string=True) #query_string=True --> separate cache per filter combo (/treks, /treks?difficulty=easy, etc.)
def get_treks():
    # delay 2 seconds
    time.sleep(2)
    try:
        query = TrekModel.query.filter_by(status=TrekStatus.OPEN)

        difficulty = request.args.get("difficulty")
        location = request.args.get("location")
        duration = request.args.get("duration")
        search = request.args.get("search")

        if difficulty:
            query = query.filter(TrekModel.difficulty == difficulty)

        if location:
            query = query.filter(TrekModel.location == location)

        if duration:
            query = query.filter(TrekModel.duration == duration)

        if search:
            query = query.filter(TrekModel.name.contains(search))

        treks = query.order_by(TrekModel.created_at.desc()).all()

        treks_json = [trek_serializer(trek) for trek in treks]

        response = {
            "message": "Treks fetched successfully.",
            "treks": treks_json,
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error occurred while fetching treks: {e}")
        return (
            jsonify({"message": "An error occurred while fetching treks."}),
            500,
        )


# get full details of one trek before booking
@trekker_bp.route("/treks/<int:trek_id>", methods=["GET"])
@jwt_required()
@role_required(UserRole.TREKKER)
def get_trek_details(trek_id):
    trek = TrekModel.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found."}), 404

    trek_json = trek_serializer(trek)

    return (
        jsonify(
            {
                "message": "Trek details fetched successfully.",
                "trek_details": trek_json,
            }
        ),
        200,
    )


# see all bookings made by the logged in trekker
@trekker_bp.route("/bookings", methods=["GET"])
@jwt_required()
@role_required(UserRole.TREKKER)
def get_trekker_bookings():
    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404

    bookings = BookingModel.query.filter_by(user_id=user.id).all()

    bookings_json = [booking_serializer(booking) for booking in bookings]

    return (
        jsonify(
            {
                "message": "Trekker bookings fetched successfully.",
                "bookings": bookings_json,
            }
        ),
        200,
    )


# book a slot on an open trek (re-book works if previously canceled)
## clear the trekker_open_treks cache after booking a trek
@trekker_bp.route("/booktrek", methods=["POST"])
@jwt_required()
@role_required(UserRole.TREKKER)
def book_trek():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404

    trek_id = data.get("trek_id")

    if not trek_id:
        return jsonify({"message": "Trek ID is required."}), 400

    trek = TrekModel.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found."}), 404

    if trek.status != TrekStatus.OPEN:
        return jsonify({"message": "Trek is not open for booking."}), 400

    if trek.available_slots <= 0:
        return jsonify({"message": "No available slots for this trek."}), 400

    existing_booking = BookingModel.query.filter_by(
        user_id=user.id, trek_id=trek.id
    ).first()

    if (
        existing_booking
    ):  # if booked already then return error message and if booked but canceled then allow to book again
        if existing_booking.status == BookingStatus.CANCELED:
            existing_booking.status = BookingStatus.BOOKED
            existing_booking.booking_date = datetime.utcnow()
            existing_booking.payment_status = PaymentStatus.PENDING
            existing_booking.amount_paid = 0.0

            trek.available_slots -= 1
            db.session.commit()

            ## clear the trekker_open_treks cache after booking a trek
            clear_trekker_open_treks_cache()

            return (
                jsonify(
                    {
                        "message": "Trek booked successfully.",
                        "booking_details": booking_serializer(existing_booking),
                    }
                ),
                200,
            )
        return jsonify({"message": "You have already booked this trek."}), 400

    new_booking = BookingModel(
        user_id=user.id,
        trek_id=trek.id,
        booking_date=datetime.utcnow(),
        status=BookingStatus.BOOKED,
        payment_status=PaymentStatus.PENDING,
        amount_paid=0.0,
    )

    try:
        db.session.add(new_booking)
        trek.available_slots -= 1
        db.session.commit()
        clear_trekker_open_treks_cache()
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while booking trek: {e}")
        return (
            jsonify({"message": "An error occurred while booking the trek."}),
            500,
        )

    return (
        jsonify(
            {
                "message": "Trek booked successfully.",
                "booking_details": booking_serializer(new_booking),
            }
        ),
        201,
    )


# cancel a booking and put the trek slot back
## clear the trekker_open_treks cache after canceling a booking
@trekker_bp.route("/deletebooking/<int:booking_id>", methods=["GET"])
@jwt_required()
@role_required(UserRole.TREKKER)
def cancel_booking(booking_id):
    user_id = int(get_jwt_identity())
    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404

    booking = BookingModel.query.get(booking_id)

    if not booking:
        return jsonify({"message": "Booking not found."}), 404

    if booking.user_id != user.id:
        return (
            jsonify({"message": "You are not authorized to cancel this booking."}),
            403,
        )

    if booking.status != BookingStatus.BOOKED:
        return jsonify({"message": "Only booked treks can be canceled."}), 400

    try:
        booking.status = BookingStatus.CANCELED
        booking.payment_status = PaymentStatus.FAILED
        booking.trek.available_slots += 1
        booking.booking_cancel_date = datetime.utcnow()
        db.session.commit()

        ## clear the trekker_open_treks cache after canceling a booking
        clear_trekker_open_treks_cache()

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while canceling booking: {e}")
        return (
            jsonify({"message": "An error occurred while canceling the booking."}),
            500,
        )

    return (
        jsonify(
            {
                "message": "Booking canceled successfully.",
                "booking_details": booking_serializer(booking),
            }
        ),
        200,
    )


# get full trekking history for the logged in trekker
@trekker_bp.route("/history", methods=["GET"])
@jwt_required()
@role_required(UserRole.TREKKER)
def get_trekking_history():
    try:
        user_id = int(get_jwt_identity())
        user = UserModel.query.get(user_id)

        if not user:
            return jsonify({"message": "User not found."}), 404

        bookings = (
            BookingModel.query.filter(
                BookingModel.user_id == user.id
            )
            .order_by(BookingModel.booking_date.desc())
            .all()
        )

        history_json = []

        for booking in bookings:

            trek = trek_serializer(booking.trek)

            # Add booking information to the trek
            trek["booking_id"] = booking.id
            trek["booking_status"] = booking.status.value
            trek["payment_status"] = booking.payment_status.value
            trek["booking_date"] = booking.booking_date.strftime("%d %b %Y")

            history_json.append(trek)

        return (
            jsonify(
                {
                    "message": "Trekking history fetched successfully.",
                    "history": history_json,
                }
            ),
            200,
        )

    except Exception as e:
        print(f"Error occurred while fetching trekking history: {e}")

        return (
            jsonify(
                {
                    "message": "An error occurred while fetching trekking history.",
                }
            ),
            500,
        )




# ASYNC JOB SERIALIZER

def export_job_serializer(job):
    return {
        "id": job.id,
        "status": job.status.value if job.status else None,
        "type_of_report": job.type_of_report.value if job.type_of_report else None,
        "file_path": os.path.basename(job.file_path) if job.file_path else None,
        "created_at": job.created_at.strftime("%Y-%m-%d %H:%M:%S") if job.created_at else None,
    }


# queue async CSV export of trekking history
@trekker_bp.route("/export-history", methods=["POST"])
@jwt_required()
@role_required(UserRole.TREKKER)
def start_export_history():
    try:
        user_id = int(get_jwt_identity())
        user = UserModel.query.get(user_id)

        if not user:
            return jsonify({"message": "User not found."}), 404

        job = ExportJobModel(
            user_id=user.id,
            status=ExportStatus.PENDING,
            type_of_report=ReportType.TREKKING_HISTORY,
        )
        db.session.add(job)
        db.session.commit()

        from tasks import export_trekker_history_csv

        export_trekker_history_csv.delay(job.id)

        return jsonify({
            "message": "Export started. You will be notified when your CSV is ready.",
            "job_id": job.id,
        }), 202

    except Exception as e:
        db.session.rollback()
        print(f"Error starting export job: {e}")
        return jsonify({"message": "An error occurred while starting export."}), 500


# list past export jobs for the logged-in trekker
@trekker_bp.route("/export-jobs", methods=["GET"])
@jwt_required()
@role_required(UserRole.TREKKER)
def list_export_jobs():
    user_id = int(get_jwt_identity())
    jobs = (
        ExportJobModel.query.filter_by(user_id=user_id)
        .order_by(ExportJobModel.created_at.desc())
        .all()
    )
    jobs_json = [export_job_serializer(job) for job in jobs]

    return jsonify({
        "message": "Export jobs fetched successfully.",
        "export_jobs": jobs_json,
    }), 200


# download completed CSV export (trekker can only download their own)
@trekker_bp.route("/export/<int:job_id>/download", methods=["GET"])
@jwt_required()
@role_required(UserRole.TREKKER)
def download_export(job_id):
    user_id = int(get_jwt_identity())
    job = ExportJobModel.query.get(job_id)

    if not job or job.user_id != user_id:
        return jsonify({"message": "Export job not found."}), 404

    if job.status != ExportStatus.COMPLETED or not job.file_path:
        return jsonify({"message": "Export is not ready yet."}), 400

    if not os.path.isfile(job.file_path):
        return jsonify({"message": "Export file not found on server."}), 404

    return send_file(
        job.file_path,
        as_attachment=True,
        download_name=os.path.basename(job.file_path),
        mimetype="text/csv",
    )
