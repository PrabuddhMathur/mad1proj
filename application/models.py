from .database import *
from flask_security import UserMixin, RoleMixin


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class User(db.Model, UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    email=db.Column(db.String, unique=True)
    username=db.Column(db.String)
    password=db.Column(db.String(255))
    active=db.Column(db.Boolean())
    roles=db.relationship('Role', secondary="roles_users")
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)

class Role(db.Model, RoleMixin):
    __tablename__='role'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class venue(db.Model):
    __tablename__='venue'
    venue_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_name=db.Column(db.String, unique=True)
    venue_place=db.Column(db.String)
    venue_location=db.Column(db.String)
    venue_capacity=db.Column(db.Integer)
    venue_show=db.relationship("show", secondary="show_venue", backref="show_venue")

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
    booking_tickets=db.Column(db.Integer, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    show_id=db.Column(db.Integer, db.ForeignKey("show.show_id"), nullable=False)
    user_rating=db.Column(db.Integer)

class show_venue(db.Model):
    __tablename__='show_venue'
    show_venue_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_id=db.Column(db.Integer, db.ForeignKey("show.show_id"), nullable=False)
    venue_id=db.Column(db.Integer, db.ForeignKey("venue.venue_id"), nullable=False)
    available_tickets=db.Column(db.Integer, nullable=True)

