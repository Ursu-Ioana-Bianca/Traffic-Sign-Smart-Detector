from flask import Blueprint, render_template

page_blueprint = Blueprint('pages', __name__)

@page_blueprint.route('/home')
def home_page():
    return render_template('index.html')

@page_blueprint.route('/about')
def about_page():
    return render_template('about.html')

@page_blueprint.route('/help')
def help_page():
    return render_template('help.html')
