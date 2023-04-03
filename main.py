from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_login import LoginManager
from application.views import *
from application.auth import *

app=None

def create_app():
    app=Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    app.app_context().push()
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    
    db.create_all()

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return user.query.filter_by(email=id).first()

    return app

app=create_app()

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080)
