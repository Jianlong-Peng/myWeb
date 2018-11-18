from flask import Flask, redirect, url_for, flash, render_template
from flask_wtf import CSRFProtect
from flask_login import current_user
## from flask_principal import identity_loaded, UserNeed, RoleNeed
## from flask_wtf.csrf import CsrfProtect
## from config import DevConfig
from .models import db
from .controllers.expense import expense_blueprint
from .controllers.main import main_blueprint
from .controllers.index import index_blueprint
from .controllers.food import food_blueprint
from .extensions import bcrypt, login_manager, debug_toolbar #, principals #, oid

def create_app(object_name):
    ## csrf = CsrfProtect()

    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    ## oid.init_app(app)
    ## csrf.init_app(app)
    CSRFProtect(app)
    login_manager.init_app(app)
    ## principals.init_app(app)
    debug_toolbar.init_app(app)

    ## @identity_loaded.connect_via(app)
    ## def on_identity_loaded(sender, identity):
    ##     #set the identity user object
    ##     identity.user = current_user
    ##     
    ##     #Add the UserNeed to the identity
    ##     if hasattr(current_user, 'id'):
    ##         identity.provides.add(UserNeed(current_user.id))
    ##     
    ##     # Add each role to the identity
    ##     if hasattr(current_user, 'roles'):
    ##         for role in current_user.roles:
    ##             identity.provides.add(RoleNeed(role.name))
    
    ## @app.route("/")
    ## def index():
    ##     ## flash("current_user: {}".format(current_user), category="debug")
    ##     ## flash("current_user.is_anonymous(): <{}>".format(current_user.is_anonymous()), category="debug")
    ##     if current_user.is_anonymous==True or current_user.is_anonymous():
    ##         return redirect(url_for('main.login'))
    ##     else:
    ##         return render_template("index.html")
    ##         ## return redirect(url_for('blog.home'))
    
    
    app.register_blueprint(index_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(expense_blueprint)
    app.register_blueprint(food_blueprint)

    return app


