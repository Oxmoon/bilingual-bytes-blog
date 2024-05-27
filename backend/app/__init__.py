import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler
from smtplib import SMTPHeloError, SMTPNotSupportedError
from urllib.parse import urljoin

from flask import Flask, flash

from config import config

from .extensions import csrf, db, email, login, mail, migrate


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    app = Flask(__name__, static_folder="staticfiles")
    app.config.from_object(config[config_name])

    initialize_extensions(app)
    register_blueprints(app)
    # configure_logging(app)

    return app


def register_blueprints(app):
    from app.auth import bp as auth_bp
    from app.errors import bp as errors_bp
    from app.main import bp as main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(errors_bp, url_prefix="/errors")
    app.register_blueprint(main_bp)


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    email.init_app(app)
    csrf.init_app(app)


def flash_errors(form):
    if len(form.errors) > 0:
        flash("Errors in form, please try again", "error")
    else:
        flash("An error has occured", "error")


# def configure_logging(app):
#     if not app.debug and not app.testing:
#         if app.config["MAIL_SERVER"]:
#             auth = None
#             if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
#                 auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
#             secure = None
#             if app.config["MAIL_USE_TLS"]:
#                 secure = ()
#             try:
#                 mail_handler = SMTPHandler(
#                     mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
#                     fromaddr=f"logs@{app.config['DOMAIN']}",
#                     toaddrs=app.config["ADMINS"],
#                     subject="Portal Failure",
#                     credentials=auth,
#                     secure=secure,
#                 )
#             except (SMTPHeloError, SMTPNotSupportedError) as e:
#                 error_code = e.smtp_code
#                 error_message = e.smtp_error
#                 print(error_code, error_message)
#             mail_handler.setLevel(logging.ERROR)
#             app.logger.addHandler(mail_handler)
#
#         if app.config["LOG_TO_STDOUT"]:
#             stream_handler = logging.StreamHandler()
#             stream_handler.setLevel(logging.INFO)
#             app.logger.addHandler(stream_handler)
#         else:
#             if not os.path.exists("logs"):
#                 os.mkdir("logs")
#             file_handler = RotatingFileHandler(
#                 "logs/portal.log", maxBytes=10240, backupCount=10
#             )
#             file_handler.setFormatter(
#                 logging.Formatter(
#                     "%(asctime)s %(levelname)s: %(message)s "
#                     "[in %(pathname)s:%(lineno)d]"
#                 )
#             )
#             file_handler.setLevel(logging.INFO)
#             app.logger.addHandler(file_handler)
#
#         app.logger.setLevel(logging.INFO)
#         app.logger.info("Portal startup")
