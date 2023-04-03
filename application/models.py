from .database import db
from flask_security import UserMixin, RoleMixin

class user(db.Model, UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    email=db.Column(db.String)
    username=db.Column(db.String, unique=True)
    password=db.Column(db.String(255))
    active=db.Column(db.Boolean())
    roles=db.relationship('role', secondary="roles_users")
    def is_active(self):
    #all users are active
        return True 

    def get_id(self):
        # returns the user e-mail. not sure who calls this
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        # False as we do not support annonymity
        return False


class role(db.Model, RoleMixin):
    __tablename__='role'
    role_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(80), unique=True)

class roles_users(db.Model):
    __tablename__='roles_users'
    roles_users_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    role_id=db.Column(db.Integer, db.ForeignKey("role.role_id"))

class venue(db.Model):
    __tablename__='venue'
    venue_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_name=db.Column(db.String)
    venue_place=db.Column(db.String)
    venue_location=db.Column(db.String)
    venue_capacity=db.Column(db.Integer)
    venue_show=db.relationship("show", secondary="show_venue")

class show(db.Model):
    __tablename__='show'
    show_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_name=db.Column(db.String)
    show_timing=db.Column(db.String)
    show_rating=db.Column(db.Integer)
    show_tags=db.Column(db.String)
    show_ticketprice=db.Column(db.Integer)

class bookings(db.Model):
    __tablename__="bookings"
    booking_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    show_venue_id=db.Column(db.Integer, db.ForeignKey("show_venue.show_venue_id"), nullable=False)
    user_rating=db.Column(db.Integer)

class show_venue(db.Model):
    __tablename__='show_venue'
    show_venue_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_id=db.Column(db.Integer, db.ForeignKey("show.show_id"), nullable=False)
    venue_id=db.Column(db.Integer, db.ForeignKey("venue.venue_id"), nullable=False)
    available_tickets=db.Column(db.Integer, nullable=True)

