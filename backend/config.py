import os
from datetime import timedelta
from pathlib import Path

from dotenv.main import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    BASE_DIR = Path(__file__).parent
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    ADMINS = os.environ.get("ADMINS")

    # in MB
    MAX_CONTENT_LENGTH = 100 * 1024 * 1000


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    STAGING = True


class StagingConfig(Config):
    DEBUG = False
    TESTING = False
    STAGING = True


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    STAGING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    STAGING = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "staging": StagingConfig,
}
