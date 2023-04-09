import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG=False
    SQLITE_DB_DIR=None
    SQLALCHEMY_DATABASE_URI=None
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR=os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")
    DEBUG=True
    SECRET_KEY="ksaldf234iuo234jbkj"
    SECURITY_PASSWORD_HASH="bcrypt"
    SECURITY_PASSWORD_SALT="laksdnvlwr809384asnvlkj"
    SECURITY_REGISTERABLE=True
    SECURITY_SEND_REGISTER_EMAIL=False
    SECURITY_LOGIN_USER_TEMPLATE="security/user_login.html"
    SECURITY_REGISTER_USER_TEMPLATE="security/user_register.html"
    WTF_CSRF_ENABLED=False
    SECURITY_CONFIRMABLE=False
    SECURITY_USERNAME_ENABLE=True

