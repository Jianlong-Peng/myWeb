import os
from flask import render_template, Blueprint, redirect, url_for, session, g, flash, abort, request
from flask_login import login_required, current_user
import datetime

food_blueprint = Blueprint(
    'food',
    __name__,
    template_folder = os.path.join(os.path.pardir, 'templates','food'),
    url_prefix="/food"
)


@food_blueprint.route("/")
@login_required
def home():
    return render_template('home.html')

