from flask import Blueprint, render_template

homepage = Blueprint('homepage', __name__)

@homepage.route('/', endpoint='homepage')
def homepage_view():
    return render_template('homepage.html')

@homepage.route('/about', endpoint='about')
def about_page():
    return render_template('homepage.html')
