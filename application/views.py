from flask import Blueprint, render_template, redirect,request,flash, url_for
from flask_security import login_required, current_user
from .models import *

views=Blueprint('views', __name__)

@views.route("/", methods=["GET","POST"])
def home():
    return render_template("home.html", user=current_user)

@views.route("/user_dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():
    venues=venue.query.all()
    shows=show.query.all()
    show_venues=show_venue.query.all()
    return render_template("user_dashboard.html",venues=venues,shows=shows, user=current_user, show_venues=show_venues)

@views.route("/user_bookings", methods=["GET","POST"])
@login_required
def user_bookings():
    venues=venue.query.all()
    shows=show.query.all()
    show_venues=show_venue.query.all()
    show_bookings=bookings.query.all()
    return render_template("user_bookings.html", venues=venues, shows=shows, show_venues=show_venues,show_bookings=show_bookings)

@views.route("/admin_dashboard", methods=["GET", "POST"])
@login_required
def admin_dashboard():
    venues=venue.query.all()
    shows=show.query.all()
    show_venues=show_venue.query.all()
    return render_template("admin_dashboard.html", venues=venues, shows=shows, show_venues=show_venues)

@views.route("/admin_summary", methods=["GET", "POST"])
@login_required
def admin_summary():
    return render_template("admin_summary.html")

@views.route("/create/venue", methods=["POST"])
def create_venue():
    venue_name=request.form.get('venue')
    venue_place=request.form.get('place')
    venue_location=request.form.get('location')
    venue_capacity=request.form.get('capacity')

    from application.database import db
    new_venue=venue(venue_name=venue_name, venue_place=venue_place, venue_location=venue_location, venue_capacity=venue_capacity)

    db.session.add(new_venue)
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/edit/venue/<int:venue_id>", methods=["POST"])
def edit_venue(venue_id):
    new_venue=venue.query.filter_by(venue_id=venue_id).first()

    new_venue.venue_name=request.form.get('venue')
    new_venue.venue_place=request.form.get('place')
    new_venue.venue_location=request.form.get('location')
    new_venue.venue_capacity=request.form.get('capacity')

    from application.database import db
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/delete/venue/<int:venue_id>", methods=["GET"])
def delete_venue(venue_id):
    venue_details=venue.query.get(venue_id)
    show_venue_details=show_venue.query.filter_by(venue_id=venue_id).all()
    show_details=[show.query.filter_by(show_id=i.show_id).first() for i in show_venue_details]

    from application.database import db
    db.session.delete(venue_details)
    [db.session.delete(i) for i in show_venue_details]
    [db.session.delete(i) for i in show_details]
    db.session.commit()
    return redirect(url_for('views.admin_dashboard'))

@views.route("/create/show/<int:venue_id>", methods=["POST"])
def create_show(venue_id):

    venue_=venue.query.filter_by(venue_id=venue_id).first()

    show_name=request.form.get('show_name')
    show_timing=request.form.get('show_timing')
    show_rating=request.form.get('show_rating')
    show_tags=request.form.get('show_tags')
    show_ticketprice=request.form.get('show_price')
    show_available_tickets=request.form.get('available_tickets')

    if int(show_available_tickets)>venue_.venue_capacity:
        flash("Tickets cannot be more than venue capacity!")
    else:
        from application.database import db
        new_show=show(show_name=show_name, show_timing=show_timing, show_rating=show_rating, show_tags=show_tags, show_ticketprice=show_ticketprice)

        db.session.add(new_show)
        db.session.flush()
        db.session.refresh(new_show)

        new_show_venue=show_venue(show_id=new_show.show_id, venue_id=venue_id, available_tickets=show_available_tickets)
        db.session.add(new_show_venue)
        db.session.commit()
        return redirect(url_for("views.admin_dashboard"))

@views.route("/edit/show/<int:show_id>", methods=["POST"])
def edit_show(show_id):
    new_show=show.query.filter_by(show_id=show_id).first()
    new_show_venue=show_venue.query.filter_by(show_id=show_id).first()

    new_show.show_name=request.form.get('show_name')
    new_show.show_timing=request.form.get('show_timing')
    new_show.show_rating=request.form.get('show_rating')
    new_show.show_tags=request.form.get('show_tags')
    new_show.show_ticketprice=request.form.get('show_price')
    new_show_venue.show_available_tickets=request.form.get('available_tickets')

    from application.database import db
    db.session.commit()
    return redirect(url_for('views.admin_dashboard'))


@views.route("/delete/show/<int:show_id>", methods=["GET"])
def delete_show(show_id):
    show_details=show.query.get(show_id)
    show_venue_details=show_venue.query.filter_by(show_id=show_id).first()

    from application.database import db
    db.session.delete(show_details)
    db.session.delete(show_venue_details)
    db.session.commit()

    return redirect(url_for("views.admin_dashboard"))

@views.route("/create/booking/<int:show_id>", methods=["POST"])
def show_booking(show_id):
    booking_tickets=request.form.get('booking_tickets')
    show_venue_details=show_venue.query.filter_by(show_id=show_id).first()

    from application.database import db

    new_booking=bookings(booking_tickets=booking_tickets, user_id=current_user.id, show_venue_id=show_venue_details.show_venue_id)
    db.session.add(new_booking)
    db.session.commit()
    return redirect(url_for("views.user_dashboard"))

@views.route("/create/rating/<int:show_id>", methods=["POST"])
def show_rating(show_id):
    return redirect(url_for('views.user_bookings'))
@views.route("/dwivedi", methods=["GET"])
def dwivedi():
    return render_template("dwivedi.html")

@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
