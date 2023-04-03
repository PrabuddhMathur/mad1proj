from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth=Blueprint('auth', __name__)

@auth.route('/login', methods=["GET","POST"])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        from .models import user, roles_users
        u=user.query.filter_by(email=email).first()
        ru=roles_users.query.filter_by(user_id=u.id).first()

        if u:
            if ru.role_id==1:
                if check_password_hash(u.password, password):
                    flash("Admin user logged in successfully!", category='success')
                    login_user(u,remember=True)
                    return redirect(url_for('views.admin_dashboard'))
                else:
                    flash("Incorrect password, try again!", category='error')
            else:
                if check_password_hash(u.password, password):
                    flash("user logged in successfully!", category='success')
                    login_user(u,remember=True)
                    return redirect(url_for('views.user_dashboard'))
                else:
                    flash("Incorrect password, try again!", category='error')
        else:
            flash("user doesnot exist!", category='error')

    return render_template("security/user_login.html", user=current_user)
        

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        repassword=request.form.get('repassword')
        username=request.form.get('username')

        from .models import user, roles_users
        u = user.query.filter_by(email=email).first()
        if u:
            flash('Email is already taken, try another email.', category='error')
        elif len(email) < 6:
            flash('Email must be greater than 5 characters.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif repassword != repassword:
            flash('Passwords don\'t match.', category='error')
        else:

            from application.database import db
            # Add user to the database
            new_user = user(email=email, username=username, password=generate_password_hash(password, method='sha256'))

            db.session.add(new_user)
            db.session.flush()
            db.session.refresh(new_user)

            new_role = roles_users(user_id=new_user.id, role_id=2)

            db.session.add(new_role)
            db.session.commit()
            flash('Successfully signed up.', category='success')
            return redirect(url_for('auth.login'))
    return render_template("security/user_register.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You\'ve been logged out.", category='success')
    return redirect(url_for('auth.login'))
