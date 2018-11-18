from flask import Blueprint, redirect, render_template, url_for, flash, session, g
from flask_login import login_user, logout_user, current_user
## from flask_principal import Identity, AnonymousIdentity, identity_changed, current_app
from webapp.forms import LoginForm, RegisterForm#, OpenIDForm
from webapp.models import db,User
## from webapp.extensions import oid
import datetime

index_blueprint = Blueprint('index', __name__, template_folder='../templates', url_prefix="/")

@index_blueprint.route("/",methods=['GET','POST'])
def index():
   return render_template("index.html")

