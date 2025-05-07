from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, logout_user
from application.bp.authentication.forms import RegisterForm, LoginForm
from application.database import db, User
authentication = Blueprint('authentication', __name__, template_folder='templates')

@authentication.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'danger')
        else:
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('authentication.login'))
    return render_template('register.html', form=form)


@authentication.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('User Not Found', 'danger')
        elif not user.check_password(form.password.data):
            flash('Password Incorrect', 'danger')
        else:
            login_user(user)
            return redirect(url_for('authentication.dashboard'))
    return render_template('login.html', form=form)

@authentication.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage.homepage'))