from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import uuid

db = SQLAlchemy()

# -----------------------------
# ✅ 예약 모델
# -----------------------------
class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    quote_no = db.Column(db.String(20), unique=True, nullable=False)
    reservation_no = db.Column(db.String(20), unique=True, nullable=False)

    customer_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    manager = db.Column(db.String(50))

    destination = db.Column(db.String(100))
    product_name = db.Column(db.String(100))

    departure_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    total_people = db.Column(db.Integer)

    status = db.Column(db.String(20), default='pending')
    memo = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ 항공/리조트/인원 필드
    flight_status = db.Column(db.String(50))
    departure_time = db.Column(db.String(20))
    return_time = db.Column(db.String(20))

    adult = db.Column(db.Integer)
    child = db.Column(db.Integer)
    infant = db.Column(db.Integer)

    resort_status = db.Column(db.String(50))
    resort_styles = db.Column(db.String(100))
    resort_name = db.Column(db.String(100))
    resort_request = db.Column(db.Text)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        now_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        self.quote_no = f"Q{now_str}{str(uuid.uuid4().hex)[:4].upper()}"
        self.reservation_no = f"R{now_str}{str(uuid.uuid4().hex)[:4].upper()}"

# -----------------------------
# ✅ 견적 모델 (추가된 부분)
# -----------------------------
class Quote(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.String(20), unique=True, nullable=False)

    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    destination = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    adult_count = db.Column(db.Integer, default=0)
    child_count = db.Column(db.Integer, default=0)
    infant_count = db.Column(db.Integer, default=0)

    flight_status = db.Column(db.String(50))
    resort_style = db.Column(db.String(50))
    resort_status = db.Column(db.String(50))

    requirements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
