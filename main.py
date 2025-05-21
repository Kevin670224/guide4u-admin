from flask import Flask
from models import db
import models  # 테이블 정의 인식용

def create_app():
    app = Flask(__name__, template_folder='templates')

    # 🔧 DB 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 🔧 DB 초기화
    db.init_app(app)

    # 🔧 블루프린트 등록
    from routes.admin_reservation import admin_reservation_bp
    from routes.admin_dashboard import admin_dashboard_bp
    from routes.quote import quote_bp

    app.register_blueprint(admin_reservation_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(quote_bp)

    # 🔧 관리자 기본 라우트
    @app.route("/admin")
    def admin_home():
        from flask import render_template
        return render_template("admin/dashboard.html")

    return app

# ✅ 실제 실행부
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
