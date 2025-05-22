from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
from io import BytesIO
from openpyxl import Workbook
from datetime import datetime
from models import db
from models import Reservation

admin_reservation_bp = Blueprint("admin_reservation", __name__, url_prefix="/admin")


# ✅ 예약 목록 페이지 (필터 + 페이징)
@admin_reservation_bp.route("/reservations")
def admin_reservations():
    customer_name = request.args.get("customer_name", "").strip()
    reservation_code = request.args.get("reservation_code", "").strip()
    departure_date = request.args.get("departure_date", "").strip()
    date_range = request.args.get("date_range", "").strip()
    destination = request.args.get("destination", "").strip()
    status = request.args.get("status", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Reservation.query

    if customer_name:
        query = query.filter(Reservation.customer_name.ilike(f"%{customer_name}%"))
    if reservation_code:
        query = query.filter(Reservation.reservation_no.ilike(f"%{reservation_code}%"))
    if departure_date:
        try:
            date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()
            query = query.filter(Reservation.departure_date == date_obj)
        except ValueError:
            pass
    if date_range and "to" in date_range:
        try:
            start_str, end_str = date_range.split("to")
            start_date = datetime.strptime(start_str.strip(), "%Y-%m-%d").date()
            end_date = datetime.strptime(end_str.strip(), "%Y-%m-%d").date()
            query = query.filter(Reservation.departure_date.between(start_date, end_date))
        except ValueError:
            pass
    if destination:
        query = query.filter(Reservation.destination.ilike(f"%{destination}%"))
    if status:
        query = query.filter(Reservation.status == status)

    per_page = 10
    pagination = query.order_by(Reservation.created_at.desc()).paginate(page=page, per_page=per_page)
    reservations = pagination.items
    total_count = pagination.total

    return render_template("admin/reservations.html",
                           reservations=reservations,
                           pagination=pagination,
                           total_count=total_count,
                           customer_name=customer_name,
                           reservation_code=reservation_code,
                           departure_date=departure_date,
                           date_range=date_range,
                           destination=destination,
                           status=status)


# ✅ 예약 상세 페이지
@admin_reservation_bp.route("/reservation/<reservation_id>")
def reservation_detail(reservation_id):
    return render_template("admin/reservation_detail.html", reservation_id=reservation_id)


# ✅ 엑셀 다운로드
@admin_reservation_bp.route("/reservations/download")
def download_reservations_excel():
    customer_name = request.args.get("customer_name", "").strip()
    reservation_code = request.args.get("reservation_code", "").strip()
    departure_date = request.args.get("departure_date", "").strip()
    date_range = request.args.get("date_range", "").strip()
    destination = request.args.get("destination", "").strip()
    status = request.args.get("status", "").strip()

    query = Reservation.query

    if customer_name:
        query = query.filter(Reservation.customer_name.ilike(f"%{customer_name}%"))
    if reservation_code:
        query = query.filter(Reservation.reservation_no.ilike(f"%{reservation_code}%"))
    if departure_date:
        try:
            date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()
            query = query.filter(Reservation.departure_date == date_obj)
        except ValueError:
            pass
    if date_range and "to" in date_range:
        try:
            start_str, end_str = date_range.split("to")
            start_date = datetime.strptime(start_str.strip(), "%Y-%m-%d").date()
            end_date = datetime.strptime(end_str.strip(), "%Y-%m-%d").date()
            query = query.filter(Reservation.departure_date.between(start_date, end_date))
        except ValueError:
            pass
    if destination:
        query = query.filter(Reservation.destination.ilike(f"%{destination}%"))
    if status:
        query = query.filter(Reservation.status == status)

    reservations = query.order_by(Reservation.created_at.desc()).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "예약 목록"

    headers = ["예약번호", "견적번호", "고객명", "상품명", "여행지", "출발일", "예약일", "인원", "상태"]
    ws.append(headers)

    for res in reservations:
        ws.append([
            res.reservation_no,
            res.quote_no,
            res.customer_name,
            res.product_name,
            res.destination,
            res.departure_date.strftime("%Y-%m-%d") if res.departure_date else "",
            res.created_at.strftime("%Y-%m-%d") if res.created_at else "",
            res.total_people,
            res.status,
        ])

    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return send_file(file_stream,
                     download_name="reservations.xlsx",
                     as_attachment=True,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ✅ 예약 등록 폼 페이지 (GET + POST)
@admin_reservation_bp.route("/reservation/create", methods=["GET", "POST"])
def create_reservation():
    if request.method == "POST":
        try:
            resort_styles = request.form.getlist("resort_styles")
            new_reservation = Reservation(
                customer_name=request.form["customer_name"],
                phone=request.form.get("phone"),
                manager="",  # 로그인 기능이 없다면 공백으로 처리

                destination=request.form.get("destination"),
                product_name=request.form.get("product", ""),

                departure_date=request.form.get("departure_date"),
                return_date=request.form.get("return_date"),
                departure_time=request.form.get("departure_time"),
                return_time=request.form.get("return_time"),

                adult=int(request.form.get("adult", 0)),
                child=int(request.form.get("child", 0)),
                infant=int(request.form.get("infant", 0)),
                total_people=int(request.form.get("adult", 0)) +
                             int(request.form.get("child", 0)) +
                             int(request.form.get("infant", 0)),

                flight_status=request.form.get("flight_status"),
                resort_status=request.form.get("resort_status"),
                resort_styles=", ".join(resort_styles),
                resort_name=request.form.get("resort_name"),
                resort_request=request.form.get("resort_request"),

                status=request.form.get("status"),
                created_at=datetime.utcnow()
            )

            db.session.add(new_reservation)
            db.session.commit()
            flash("✅ 예약이 성공적으로 등록되었습니다!", "success")
            return redirect("/admin/reservations")

        except Exception as e:
            print("❌ 등록 중 오류:", e)
            flash("❌ 예약 등록 중 오류가 발생했습니다.", "danger")
            return redirect("/admin/reservation/create")

    return render_template("admin/create_reservation.html")
