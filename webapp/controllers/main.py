from flask import Blueprint, redirect, render_template, url_for, flash, session, g
from flask_login import login_user, logout_user, current_user
## from flask_principal import Identity, AnonymousIdentity, identity_changed, current_app
from webapp.forms import LoginForm, RegisterForm#, OpenIDForm
from webapp.models import db,User
## from webapp.extensions import oid
import datetime

main_blueprint = Blueprint('main', __name__, template_folder='../templates/main', url_prefix="/")

@main_blueprint.route("/login",methods=['GET','POST'])
## @oid.loginhandler
## def login():
##     form = LoginForm()
##     openid_form = OpenIDForm()
## 
##     if openid_form.validate_on_submit():
##         return oid.try_login(
##             openid_form.openid.data,
##             ask_for=['nickname','email'],
##             ask_for_optional=['fullname']
##         )
## 
##     if form.validate_on_submit():
##         flash("Welcome {0}".format(form.username.data), category="success")
##         return redirect(url_for('blog.home'))
## 
##     openid_errors = oid.fetch_error()
##     if openid_errors:
##         flash(openid_errors, category="danger")
## 
##     if form.errors:
##         flash(form.errors)
## 
##     return render_template('login.html',form=form,openid_form=openid_form)
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data, duration=datetime.timedelta(int(form.duration.data)))
        ## session['username'] = form.username.data
        ## identity_changed.send(
        ##     current_app._get_current_object(),
        ##     identity=Identity(user.id)
        ## )
        ## flash("Welcome {0}".format(current_user), category="success")
        return redirect(url_for('index.index'))

    ## if form.errors:
    ##     flash(form.errors)

    return render_template("login.html", form=form)

@main_blueprint.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    ## g.current_user = None
    ## ## session.pop('username',None)
    ## identity_changed.send(
    ##     current_app._get_current_object(),
    ##     identity=AnonymousIdentity()
    ## )
    ## flash("You have been logged out.", category="success")
    return redirect(url_for('main.login'))

@main_blueprint.route("/register",methods=['GET','POST'])
## @oid.loginhandler
## def register():
##     form = RegisterForm()
##     openid_form = OpenIDForm()
## 
##     if openid_form.validate_on_submit():
##         return oid.try_login(
##             openid_form.openid.data,
##             ask_for = ['nickname','email'],
##             ask_for_optional = ['fullname']
##         )
## 
##     if form.validate_on_submit():
##         new_user = User(form.username.data)
##         new_user.set_password(form.password.data)
##         db.session.add(new_user)
##         db.session.commit()
## 
##         flash("Your user has been created, please login.", category="success")
##         return redirect(url_for('user.login'))
## 
##     openid_errors = oid.fetch_error()
##     if openid_errors:
##         flash(openid_errors, category="danger")
## 
##     if form.errors:
##         flash(form.errors)
## 
##     return render_template('register.html', form=form, openid_form=openid_form)
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data)
        ## new_user.username = form.username.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash("Your user has been created, please login.", category="success")
        return redirect(url_for('index.index'))

    ## if form.errors:
    ##     flash(form.errors)

    return render_template('register.html', form=form)

