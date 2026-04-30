from flask import Flask, render_template, request, redirect, url_for, session
from models import db, PortfolioCard
from admin import admin_bp
from flask_wtf import CSRFProtect
import os
from dotenv import load_dotenv
from src.security.password import verify_password
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail, Message

load_dotenv()
mail = Mail()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    limiter = Limiter(get_remote_address, app=app, default_limits=[])

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Логин и пароль администратора
    app.config["ADMIN_USERNAME"] = os.getenv("ADMIN_USERNAME")
    app.config["ADMIN_PASSWORD_HASH"] = os.getenv("ADMIN_PASSWORD_HASH")

    # подключение отправки письма
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True 
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    mail.init_app(app)


    # Настройки БД
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Инициализация расширений
    csrf.init_app(app)
    db.init_app(app)

    # -----------------------------
    # Авторизация
    # -----------------------------
    @limiter.limit("5 per 10 minutes")
    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if username == app.config["ADMIN_USERNAME"]:
                try:
                    if verify_password(app.config["ADMIN_PASSWORD_HASH"], password):
                        session["admin"] = True
                        return redirect(url_for("admin.admin_index"))
                except:
                    pass
            return render_template("login.html", error="Неверный логин или пароль")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("admin", None)
        return redirect(url_for("login"))

    # -----------------------------
    # Защита админки
    # -----------------------------
    @app.before_request
    def protect_admin():
        if request.path == "/admin":
            if not session.get("admin"):
                return redirect(url_for("login"))


    # Регистрация blueprint админки
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Главная страница
    @app.route("/")
    def index():
        portfolio_cards = PortfolioCard.query.all()
        return render_template("index.html", portfolio_cards=portfolio_cards, page_title="Black Sheep")

    
    @app.route("/category/<string:category_slug>")
    def category_filter(category_slug):
        cards = PortfolioCard.query.filter_by(category_slug=category_slug).all()
        return render_template("index.html", portfolio_cards=cards, active_category=category_slug)

    
    @app.route("/post/<string:slug>")
    def post_page(slug):
        card = PortfolioCard.query.filter_by(slug=slug).first_or_404()
        return render_template("post.html", card=card)

    # Service Details
    @app.route("/service-details")
    def service_details():
        return render_template("service-details.html", page_title="Servis details")


    @app.route("/contact", methods=["POST"])
    def send_message():
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Формируем письмо
        msg = Message(
            subject=f"Сообщение с сайта: {subject}",
            sender=app.config['MAIL_USERNAME'],
            recipients=["in_code_we_trust@outlook.com"]  # куда отправлять
        )

        msg.body = f"""
        Имя: {name}
        Email: {email}
        Сообщение:
        {message}
        """

        # Отправка
        try:
            mail.send(msg)
            return render_template("contact-success.html", page_title="Contact success")
        except Exception as e:
            return render_template("404.html")





    # Создание таблиц
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
