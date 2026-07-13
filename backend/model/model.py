from db.db import db  # creating model using DB object instance from  db.py
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

# Enums


# userRoles
class UserRole(str, Enum):
    ADMIN = "admin"
    TREKKER = "trekker"
    STAFF = "staff"


# trekdifficulty
class TrekDifficulty(str, Enum):
    EASY = "easy"
    MODERATE = "moderate"
    DIFFICULT = "difficult"


# trekstatus
class TrekStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    OPEN = "open"
    ONGOING = "ongoing"
    CLOSED = "closed"
    COMPLETED = "completed"


# BookingStatus
class BookingStatus(str, Enum):
    BOOKED = "booked"
    COMPLETED = "completed"
    CANCELED = "canceled"


# PaymentStatus
class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    PAID = "paid"


# StaffStatus 
class StaffStatus(str, Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"
    BLACKLISTED = "blacklisted"


## extra enums for MAD2 
class ExportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class NotificationStatus(str, Enum):
    REMINDER = "reminder"
    BOOKING = "booking"
    REPORT = "report"
    EXPORT = "export"


class ReportType(str, Enum):
    TREKKING_HISTORY = "trekking_history"
    ANALYTICS = "analytics"
    MONTHLY = "monthly"


# Mixins {using Multiple Inheritance to create common fields for all models}
class TimeStampMixin(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

#BaseModel
class BaseModel(TimeStampMixin, db.Model):
    __abstract__ = True  ## means this class is not a table in the database, but it can be inherited by other models to have common fields [new concept of abstract base class in SQLAlchemy]
    id = db.Column(db.Integer, primary_key=True)


# Models
class UserModel(BaseModel): 

    __tablename__ = "users"

    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.TREKKER, nullable=False)

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    blacklisted_reason = db.Column(db.String(500), nullable=True)

    bookings = db.relationship(
        "BookingModel",
        backref=db.backref("user", lazy=True),
        foreign_keys="BookingModel.user_id",
        lazy=True,
        cascade="all, delete-orphan",  # if a user is deleted, all their bookings will be deleted as well
    )

    staff_profile = db.relationship(
        "StaffModel",
        backref=db.backref("user", uselist=False),
        uselist=False,
        cascade="all, delete-orphan",
    )


    ### MAD2 - PJ extra relationships using old backref style
    notifications = db.relationship(
        "NotificationModel",
        backref=db.backref("user", lazy=True),
        foreign_keys="NotificationModel.user_id",
        lazy=True,
        cascade="all, delete-orphan",
    )

    export_jobs = db.relationship(
        "ExportJobModel",
        backref=db.backref("user", lazy=True),
        foreign_keys="ExportJobModel.user_id",
        lazy=True,
        cascade="all, delete-orphan",
    )
    ###

    # methods to set and check password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Staff Model
class StaffModel(BaseModel):
    __tablename__ = "staffs"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True
    )
    
    # user relationship is now automatically handled by UserModel's staff backref

    joining_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    experience = db.Column(db.Integer, nullable=False, default=0)  # in years
    address = db.Column(db.String(200), nullable=True, default="Add your address now")
    contact_number = db.Column(
        db.String(15), nullable=True, default="Add your contact number now"
    )
    staff_bio = db.Column(db.String(500), nullable=True, default="Add your bio now")
    Profile_status = db.Column(db.Enum(StaffStatus), default=StaffStatus.PENDING, nullable=False) # matched back to v1 column name and default enum status
    

    treks = db.relationship(
        "TrekModel",
        backref=db.backref("staff", lazy=True),
        foreign_keys="TrekModel.assigned_staff_id",
        lazy=True,
    )  # one to many relationship with TrekModel


# Trek Model
class TrekModel(BaseModel):
    __tablename__ = "treks"

    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Enum(TrekDifficulty), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False, default=10)
    available_slots = db.Column(db.Integer, nullable=False, default=10)

    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(600), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    starting_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # reverted name back to starting_at from v1
    ending_at = db.Column(db.DateTime, nullable=False) # reverted name back to ending_at from v1
    status = db.Column(db.Enum(TrekStatus), default=TrekStatus.PENDING, nullable=False)

    # relationship with user model (staff) [one] to [many] Trek Model
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("staffs.id"), nullable=True)
    
    # staff relationship is now automatically handled by StaffModel's treks backref
    
    bookings = db.relationship(
        "BookingModel", backref=db.backref("trek", lazy=True), lazy=True, cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.CheckConstraint(
            "available_slots <= total_slots", name="check_available_slots"
        ),
        db.CheckConstraint("starting_at < ending_at", name="ending before start constraint"),
        db.CheckConstraint("price >= 0", name="zero_price_constraint"),
    )


class BookingModel(BaseModel):
    __tablename__ = "bookings"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)

    booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(
        db.Enum(BookingStatus), default=BookingStatus.BOOKED, nullable=False
    )
    payment_status = db.Column(
        db.Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False
    )

    amount_paid = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    booking_cancel_date = db.Column(db.DateTime, nullable=True)
    booking_cancel_reason = db.Column(db.String(500), nullable=True)

    # relationships (automatically generated via backrefs on UserModel and TrekModel)

    # constraints to ensure data integrity
    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "trek_id", name="unique_user_trek_booking"
        ),  ## only one user can book a trek at a time
    )



## MAD2PJ Models for Notification, ExportJob 

class NotificationModel(BaseModel):
    __tablename__ = "notifications"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message_text = db.Column(db.String(500), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    type_of_notification = db.Column(db.Enum(NotificationStatus) , nullable=False) 
    status = db.Column(
        db.Enum(NotificationStatus), default=NotificationStatus.REMINDER, nullable=False
    )

    # relationship automatically handled via UserModel backref side


class ExportJobModel(BaseModel):
    __tablename__ = "export_jobs"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    file_path = db.Column(db.String(200), nullable=True)
    status = db.Column(
        db.Enum(ExportStatus), default=ExportStatus.PENDING, nullable=False
    )
    type_of_report = db.Column(db.Enum(ReportType), nullable=False)

    # relationship automatically handled via UserModel backref side


class ReportLogsModel(BaseModel):
    __tablename__ = "report_logs"

    type_of_report = db.Column(db.Enum(ReportType), nullable=False)
    report_summary = db.Column(db.String(1000), nullable=True)
    status = db.Column(
        db.Enum(ExportStatus), default=ExportStatus.PENDING, nullable=False
    )
