from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_security import SQLAlchemySessionUserDatastore,Security
from application.models import *


app=None

def create_app():
    app=Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    app.app_context().push()
    
    db.create_all()

    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    app.app_context().push()

    return app

app=create_app()

from application.views import *

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8090)
