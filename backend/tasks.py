import csv
import os
from datetime import datetime

from flask import render_template
from flask_sse import sse
from sqlalchemy import func

from celery_worker import celery_app
from db.db import db
from model.model import (
    BookingModel,
    BookingStatus,
    ExportJobModel,
    ExportStatus,
    NotificationModel,
    NotificationStatus,
    PaymentStatus,
    ReportLogsModel,
    ReportType,
    TrekModel,
    TrekStatus,
    UserModel,
    UserRole,
)
from utils.email_utils import send_email

EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "exports")


def _publish_sse(user_id, data):
    channel = f"user_{user_id}"
    sse.publish(data=data, type="notification", channel=channel)




# Ping task to check if Celery is alive
@celery_app.task
def ping_task():

    print("Celery is alive!")

    return "pong"





def _month_range(reference=None):

    """Return (month_start, month_end, label) for the current calendar month."""

    now = reference or datetime.utcnow()

    month_start = datetime(now.year, now.month, 1)

    if now.month == 12:

        month_end = datetime(now.year + 1, 1, 1)

    else:

        month_end = datetime(now.year, now.month + 1, 1)

    label = month_start.strftime("%B %Y")

    return month_start, month_end, label





def _build_monthly_report_data():

    month_start, month_end, month_label = _month_range()



    treks_conducted = TrekModel.query.filter(

        TrekModel.status == TrekStatus.COMPLETED,

        TrekModel.ending_at >= month_start,

        TrekModel.ending_at < month_end,

    ).count()



    monthly_bookings = BookingModel.query.filter(

        BookingModel.booking_date >= month_start,

        BookingModel.booking_date < month_end,

    ).count()



    participants = BookingModel.query.filter(

        BookingModel.booking_date >= month_start,

        BookingModel.booking_date < month_end,

        BookingModel.status.in_([BookingStatus.BOOKED, BookingStatus.COMPLETED]),

    ).count()



    monthly_revenue = (

        db.session.query(func.sum(BookingModel.amount_paid))

        .filter(

            BookingModel.booking_date >= month_start,

            BookingModel.booking_date < month_end,

            BookingModel.payment_status == PaymentStatus.PAID,

        )

        .scalar()

        or 0

    )



    popular_treks = (

        db.session.query(

            TrekModel.name.label("trek_name"),

            func.count(BookingModel.id).label("booking_count"),

        )

        .join(BookingModel, BookingModel.trek_id == TrekModel.id)

        .filter(

            BookingModel.booking_date >= month_start,

            BookingModel.booking_date < month_end,

        )

        .group_by(TrekModel.id)

        .order_by(func.count(BookingModel.id).desc())

        .limit(5)

        .all()

    )



    completed_treks = TrekModel.query.filter(

        TrekModel.status == TrekStatus.COMPLETED,

        TrekModel.ending_at >= month_start,

        TrekModel.ending_at < month_end,

    ).all()



    return {

        "month_label": month_label,

        "treks_conducted": treks_conducted,

        "participants": participants,

        "total_monthly_bookings": monthly_bookings,

        "monthly_revenue": float(monthly_revenue),

        "popular_treks": [

            {"trek_name": row.trek_name, "booking_count": row.booking_count}

            for row in popular_treks

        ],

        "completed_trek_names": [trek.name for trek in completed_treks],

    }





# Daily trek alert — notify trekkers about approved (on the way) and open (book now) treks

@celery_app.task
def send_daily_trek_reminder():

    approved_treks = TrekModel.query.filter_by(status=TrekStatus.APPROVED).order_by(

        TrekModel.starting_at.asc()

    ).all()



    open_treks = TrekModel.query.filter_by(status=TrekStatus.OPEN).order_by(

        TrekModel.starting_at.asc()

    ).all()



    print(f"Approved treks: {len(approved_treks)}, Open treks: {len(open_treks)}")



    if not approved_treks and not open_treks:

        print("Daily alert: no approved/open treks — skipping emails")

        return "No treks to announce — 0 email(s) sent"



    trekkers = UserModel.query.filter_by(

        role=UserRole.TREKKER,

        is_active=True,

        is_blacklisted=False,

    ).all()



    print(f"Active trekkers to notify: {len(trekkers)}")



    email_count = 0
    notified_ids = []

    for trekker in trekkers:

        html_body = render_template(

            "upcoming_treks.html",

            trekker_name=trekker.username,

            approved_treks=approved_treks,

            open_treks=open_treks,

            approved_count=len(approved_treks),

            open_count=len(open_treks),

        )



        send_email(
            trekker.email,
            "TrekMaster Update — New Treks On The Way & Open for Booking",
            html_body,
            content_type="html",
        )
        print(f"  Email sent to {trekker.email} ({trekker.username})")



        parts = []

        if approved_treks:

            parts.append(f"{len(approved_treks)} trek(s) on the way")

        if open_treks:

            parts.append(f"{len(open_treks)} trek(s) open for booking")



        notification = NotificationModel(

            user_id=trekker.id,

            message_text=f"Trek update: {' and '.join(parts)}.",

            type_of_notification=NotificationStatus.REMINDER,

            status=NotificationStatus.REMINDER,

        )

        db.session.add(notification)

        email_count += 1
        notified_ids.append(trekker.id)

    db.session.commit()

    parts = []
    if approved_treks:
        parts.append(f"{len(approved_treks)} trek(s) on the way")
    if open_treks:
        parts.append(f"{len(open_treks)} trek(s) open for booking")
    sse_message = f"Trek update: {' and '.join(parts)}."

    for user_id in notified_ids:
        _publish_sse(
            user_id,
            {"message": sse_message, "type": "reminder"},
        )

    print(f"Daily alert: sent {email_count} email(s)")

    return f"Sent {email_count} daily alert(s)"




# Monthly admin report — email summary to admin

@celery_app.task
def send_monthly_admin_report():

    report_data = _build_monthly_report_data()



    admin = UserModel.query.filter_by(role=UserRole.ADMIN).first()

    if not admin:

        print("Monthly report: no admin user found")

        return "No admin user — report not sent"



    html_body = render_template("monthly_report.html", report_data=report_data)



    send_email(

        admin.email,

        f"TrekMaster Monthly Report — {report_data['month_label']}",

        html_body,

        content_type="html",

    )



    report_log = ReportLogsModel(

        type_of_report=ReportType.MONTHLY,

        status=ExportStatus.COMPLETED,

    )

    db.session.add(report_log)



    notification = NotificationModel(

        user_id=admin.id,

        message_text=(

            f"Monthly report for {report_data['month_label']}: "

            f"{report_data['treks_conducted']} trek(s) conducted, "

            f"{report_data['participants']} participant(s)."

        ),

        type_of_notification=NotificationStatus.REPORT,

        status=NotificationStatus.REPORT,

    )

    db.session.add(notification)

    db.session.commit()

    report_message = (
        f"Monthly report for {report_data['month_label']}: "
        f"{report_data['treks_conducted']} trek(s) conducted, "
        f"{report_data['participants']} participant(s)."
    )
    _publish_sse(
        admin.id,
        {"message": report_message, "type": "report"},
    )

    print(
        f"Monthly report sent to {admin.email} — "
        f"{report_data['treks_conducted']} treks, {report_data['participants']} participants"
    )

    return f"Monthly report sent to {admin.email}"




# Export trekking history CSV for trekkers
@celery_app.task
def export_trekker_history_csv(export_job_id):
    """
    This task is used to export the trekking history CSV for trekkers.
    """
    job = ExportJobModel.query.get(export_job_id)

    if not job:
        print(f"Export job {export_job_id} not found")
        return "Export job not found"

    job.status = ExportStatus.PROCESSING
    db.session.commit()

    try:
        bookings = (
            BookingModel.query.filter_by(user_id=job.user_id)
            .order_by(BookingModel.booking_date.desc())
            .all()
        )

        os.makedirs(EXPORTS_DIR, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"history_user_{job.user_id}_{timestamp}.csv"
        file_path = os.path.join(EXPORTS_DIR, filename)

        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            header = [
                "Trek Name",
                "Location",
                "Difficulty",
                "Duration (Days)",
                "Start Date",
                "End Date",
                "Trek Status",
                "Booking Status",
                "Payment Status",
                "Amount Paid",
                "Booking Date",
            ]
            writer.writerow(header)

            for booking in bookings:
                trek = booking.trek
                writer.writerow([
                    trek.name if trek else "",
                    trek.location if trek else "",
                    trek.difficulty.value if trek and trek.difficulty else "",
                    trek.duration if trek else "",
                    trek.starting_at.strftime("%Y-%m-%d") if trek and trek.starting_at else "",
                    trek.ending_at.strftime("%Y-%m-%d") if trek and trek.ending_at else "",
                    trek.status.value if trek and trek.status else "",
                    booking.status.value if booking.status else "",
                    booking.payment_status.value if booking.payment_status else "",
                    float(booking.amount_paid) if booking.amount_paid is not None else 0.0,
                    booking.booking_date.strftime("%Y-%m-%d") if booking.booking_date else "",
                ])

        job.status = ExportStatus.COMPLETED
        job.file_path = file_path

        notification = NotificationModel(
            user_id=job.user_id,
            message_text="Your trekking history CSV export is ready to download.",
            type_of_notification=NotificationStatus.EXPORT,
            status=NotificationStatus.EXPORT,
        )
        db.session.add(notification)
        db.session.commit()

        _publish_sse(
            job.user_id,
            {
                "message": "Your trekking history export is ready to download.",
                "type": "export",
                "job_id": job.id,
            },
        )

        print(f"Export completed: {filename}")
        return f"Export completed: {filename}"

    except Exception as e:
        db.session.rollback()
        job.status = ExportStatus.FAILED
        db.session.commit()
        print(f"Export job {export_job_id} failed: {e}")
        return f"Export failed: {e}"


