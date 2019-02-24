from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from flask_migrate import Migrate, MigrateCommand
from webapp import create_app
from webapp.models import db, User, Account, Expense, Category, candidate_categories, Found
from webapp.forms import LoginForm, RegisterForm, QueryForm, ExpenseForm#, OpenIDForm
import os
import datetime

env = os.environ.get("WEBAPP_ENV", "dev")
app = create_app('webapp.config.%sConfig'%env.capitalize())

migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command("server",Server())
manager.add_command("db",MigrateCommand)
manager.add_command("show-urls",ShowUrls())
manager.add_command("clean",Clean())

@manager.shell
def make_shell_context():
    ## return dict(app=app, db=db, User=User)
    return dict(app=app, db=db, User=User, Account=Account, Expense=Expense, Category=Category, QueryForm=QueryForm, Found=Found, ExpenseForm=ExpenseForm)


@manager.command
def init_db():
    import random
    import datetime
    db.create_all()
    
    default = User('default')
    default.set_password("password")
    db.session.add(default)
    db.session.commit()

    for i in xrange(5):
        new_account = Account()
        new_account.name="Account {}".format(i+1)
        new_account.amount = random.random()*(i+1)
        new_account.description = "random account {}".format(i+1)
        new_account.user_id = default.id
        new_account.date = datetime.datetime.now()
        db.session.add(new_account)

    db.session.commit()

    for c in candidate_categories:
        db.session.add(Category(c))
    db.session.commit()

if __name__ == "__main__":
    manager.run()


