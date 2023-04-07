from flask import Blueprint, render_template, redirect,request,flash, url_for, jsonify
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

    search_by_category=['Show','Venue','Location','Timing', 'Genre' ]
    
    return render_template("user_dashboard.html",venues=venues,shows=shows, user=current_user, show_venues=show_venues,search_by_category=search_by_category)

@views.route("/user_dashboard/shows", methods=["GET"])
@login_required
def all_shows():
    venues=venue.query.all()
    shows=show.query.all()
    show_venues=show_venue.query.all()

    return render_template("all_shows.html",venues=venues,shows=shows, user=current_user, show_venues=show_venues)

@views.route('/user_dashboard/search/<search_value>', methods=["GET"])
def search_by(search_value):
    venues=venue.query.all()
    shows=show.query.all()
    show_venues=show_venue.query.all()

    search_by_category=['Show','Venue','Location','Timing', 'Genre' ]
    search_value=request.args.get('search_value')

    return render_template('search_by.html', venues=venues, shows=shows, show_venues=show_venues,search_by_category=search_by_category,search_value=search_value)
    


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

    genres = ['Action', 'Comedy', 'Drama', 'Horror','Mythology', 'Romance', 'Science Fiction', 'Thriller', 'Fantasy', 'Animation', 'Adventure']
    locations = ['Ahmedabad', 'Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Jaipur', 'Kanpur', 'Kolkata', 'Lucknow', 'Mumbai', 'Nagpur', 'Patna', 'Pune', 'Surat', 'Thane', 'Vadodara', 'Varanasi', 'Bhopal', 'Coimbatore', 'Visakhapatnam']
    return render_template("admin_dashboard.html", venues=venues, shows=shows, show_venues=show_venues,genres=genres,locations=locations)

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
    booking_details=[bookings.query.filter_by(show_id=i.show_id).first() for i in show_details]

    from application.database import db
    db.session.delete(venue_details)
    [db.session.delete(i) for i in show_venue_details]
    [db.session.delete(i) for i in show_details]
    [db.session.delete(i) for i in booking_details]
    db.session.commit()
    return redirect(url_for('views.admin_dashboard'))

@views.route("/create/show/<int:venue_id>", methods=["POST"])
def create_show(venue_id):

    show_name=request.form.get('show_name')
    show_timing=request.form.get('show_timing')
    show_tags=request.form.get('show_tags')
    show_ticketprice=request.form.get('show_price')
    show_available_tickets=request.form.get('available_tickets')

    from application.database import db
    new_show=show(show_name=show_name, show_timing=show_timing, show_tags=show_tags, show_ticketprice=show_ticketprice)

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
    booking_details=bookings.query.filter_by(show_id=show_id).all()

    from application.database import db
    db.session.delete(show_details)
    db.session.delete(show_venue_details)
    [db.session.delete(i) for i in booking_details]
    db.session.commit()

    return redirect(url_for("views.admin_dashboard"))

@views.route("/create/booking/<int:show_id>", methods=["POST"])
def show_booking(show_id):
    booking_tickets=request.form.get('booking_tickets')
    show_details=show.query.filter_by(show_id=show_id).first()

    from application.database import db

    new_booking=bookings(booking_tickets=booking_tickets, user_id=current_user.id, show_id=show_details.show_id)
    db.session.add(new_booking)
    db.session.commit()
    return redirect(url_for("views.user_dashboard"))

@views.route("/create/rating/<int:show_id>", methods=["POST"])
def show_rating(show_id):
    booking_details=bookings.query.filter_by(show_id=show_id).first()
    user_rating=request.form.get('rating')
    booking_details.user_rating=user_rating

    show_details=show.query.filter_by(show_id=show_id).first()
    if show_details.show_rating==None:
        show_details.show_rating=int(user_rating)
    else:
        show_details.show_rating+=int(user_rating)

    from application.database import db
    db.session.commit()

    return redirect(url_for('views.user_bookings'))
@views.route("/dwivedi", methods=["GET"])
def dwivedi():
    return render_template("dwivedi.html")

@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404