from flask import Blueprint, render_template

admin_dashboard_bp = Blueprint("admin_dashboard", __name__, url_prefix="/admin")

@admin_dashboard_bp.route("/")
def dashboard():
    return render_template("admin/dashboard.html")

@admin_dashboard_bp.route("/quotes")
def admin_quotes():
    return render_template("admin/quotes.html")

@admin_dashboard_bp.route("/reservations")
def admin_reservations():
    return render_template("admin/reservations.html")

@admin_dashboard_bp.route("/reservations/<reservation_id>")
def reservation_detail(reservation_id):
    return render_template("admin/reservation_detail.html", reservation_id=reservation_id)
