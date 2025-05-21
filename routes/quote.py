from flask import Blueprint, render_template, request, redirect
from datetime import datetime
from models import db, Quote  # Quote 모델이 models.py에 있어야 합니다

# ✅ URL prefix 추가
quote_bp = Blueprint('quote', __name__, url_prefix="/quote")

# 1. 견적 요청 폼 보여주기 (주소: /quote)
@quote_bp.route("/")
def show_quote_form():
    return render_template("quote_form.html")

# 2. 견적 저장 처리 (POST 처리 주소: /quote/submit)
@quote_bp.route("/submit", methods=["POST"])
def submit_quote():
    # 1. 견적번호 자동 생성 (예: Q20250521-001)
    today_str = datetime.today().strftime("%Y%m%d")
    today_quotes = Quote.query.filter(Quote.quote_number.like(f"Q{today_str}-%")).count() + 1
    quote_number = f"Q{today_str}-{str(today_quotes).zfill(3)}"

    # 2. 폼 데이터 저장
    new_quote = Quote(
        quote_number=quote_number,
        customer_name=request.form.get("customer_name"),
        phone=request.form.get("phone"),
        destination=request.form.get("custom_destination"),  # 직접 입력된 목적지
        start_date=request.form.get("travel_period").split(" to ")[0] if request.form.get("travel_period") else None,
        end_date=request.form.get("travel_period").split(" to ")[1] if request.form.get("travel_period") else None,
        adult_count=request.form.get("adult"),
        child_count=request.form.get("child"),
        infant_count=request.form.get("infant"),
        flight_status=request.form.get("flight_status"),
        resort_style=", ".join(request.form.getlist("resort_style")) if request.form.getlist("resort_style") else None,
        resort_status=request.form.get("resort_status"),
        resort_name=request.form.get("resort_name"),
        requirements=request.form.get("notes")
    )

    # 3. DB에 저장
    db.session.add(new_quote)
    db.session.commit()

    # 4. 완료 메시지 or 완료 페이지로 리디렉션
    return redirect("/quote")
