#encoding=utf-8
import os
from flask import render_template, Blueprint, redirect, url_for, session, g, flash, abort, request
from flask_login import login_required, current_user
## from flask_principal import Permission, UserNeed
## from config import DevConfig
## from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,and_
## from flask_wtf import Form
## from wtforms import StringField, TextAreaField
## from wtforms.validators import DataRequired, Length
import datetime
from webapp.models import db, User, Account, Expense, Category, Found
from webapp.forms import AccountForm, UpdateForm, ExpenseForm, QueryForm, TransferForm
## from webapp.extensions import poster_permission, admin_permission

expense_blueprint = Blueprint(
    'expense',
    __name__,
    template_folder = os.path.join(os.path.pardir, 'templates','expense'),
    url_prefix="/expense"
)

#### def sidebar_data():
####     recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
####     #about func, please visit http://docs.sqlalchemy.org/en/rel_1_0/core/sqlelement.html#sqlalchemy.sql.expression.func
####     top_tags = db.session.query(
####                 Tag, func.count(tags.c.post_id).label('total')
####                 ).join(
####                     tags
####                 ).group_by(Tag).order_by('total DESC').limit(5).all()
####     return recent,top_tags

## @expense_blueprint.before_request
## def check_user():
##     if 'username' in session:
##         g.current_user = User.query.filter_by(username=session['username']).one()
##     else:
##         g.current_user = None

@expense_blueprint.route("/")
@login_required
def home():
    return render_template('home.html')

@expense_blueprint.route("/account", methods=('GET','POST'))
def account():
    if current_user.is_anonymous():
        flash(current_user)
        flash("You have no right to access account. Please login first!", category="error")
        return redirect(url_for('main.login'))
    else:
        u = User.query.get_or_404(current_user.get_id())
        return render_template(
            'account.html',
            accounts = u.accounts,
            username = u.username
        )

@expense_blueprint.route("/account/new", methods=("GET","POST"))
def account_new():
    form = AccountForm()
    if form.validate_on_submit():
        if current_user.is_anonymous():
            flash(current_user)
            flash("You have no right to create new account. Please login first!", category="error")
            return redirect(url_for("main.login"))
        else:
            new_account = Account()
            new_account.name = form.name.data
            new_account.amount = float(form.amount.data)
            new_account.description = form.description.data
            new_account.user_id = int(current_user.get_id())
            new_account.date = datetime.datetime.now()
            new_found = Found()
            new_found.account_id = new_account.id
            new_found.user_id = int(current_user.get_id())
            new_found.amount = form.amount.data
            new_found.date = datetime.datetime.now()
            new_found.description = u"初始"
            db.session.add(new_found)
            db.session.add(new_account)
            db.session.commit()
            return redirect(url_for(".account"))
    return render_template("new.html", form=form)


@expense_blueprint.route("/account/update/<int:account_id>", methods=("GET","POST"))
def account_update(account_id):
    account = Account.query.get_or_404(account_id)
    if account.user_id != int(current_user.get_id()):
        abort(403)

    form = UpdateForm()

    if form.validate_on_submit():
        new_found = Found()
        new_found.account_id = account.id
        new_found.amount = form.amount.data
        new_found.date = datetime.datetime.now()
        new_found.description = form.description.data
        account.amount = form.amount.data
        account.date = datetime.datetime.now()
        db.session.add(new_found)
        db.session.add(account)
        db.session.commit()
        return redirect(url_for(".account"))

    form.amount.data = account.amount
    return render_template("update.html", form=form, account=account)

@expense_blueprint.route("/record", methods=("GET","POST"))
def record():
    form = ExpenseForm()
    form.account.choices = [(item.id,item.name) for item in Account.query.filter_by(user_id=int(current_user.get_id())).all()]
    ## if len(form.account.choices) == 0:
    ##     flash(u"你当前没有任何“资金账号”。要记录消费情况，请先创建“资金账号”。每笔消费记录将被关联到一个“资金账号”上", category="error")
    ##     return redirect(url_for(".account_new"))
    form.category.choices = [(item.id, item.category) for item in Category.query.all()]
    if form.validate_on_submit():
        if current_user.is_anonymous():
            flash("Please login first!",category="error")
            return redirect(url_for("main.login"))
        else:
            expense = Expense()
            expense.category_id = form.category.data
            expense.amount = form.amount.data
            expense.account_id = form.account.data
            expense.description = form.description.data
            expense.date = form.date.data
            expense.user_id = int(current_user.get_id())
            expense.pay = form.pay.data
            db.session.add(expense)
            db.session.commit()
            return redirect(url_for(".home"))
    return render_template("record.html", form=form)

@expense_blueprint.route("/query", methods=("GET","POST"))
def query():
    form = QueryForm()
    if form.validate_on_submit():
        if current_user.is_anonymous():
            flash("Please login first!",category="error")
            return redirect(url_for("main.login"))
        else:
            ## recent = Expense.query.filter(and_(Expense.date>=start_time, Expense.date<=end_date)).all()
            recent = Expense.query.filter(Expense.date.between(form.start_date.data,form.end_date.data)).paginate(page=1, per_page=form.per_page.data)
            ## return redirect(url_for(".show", expenses=recent.items, pagination=recent, start_date=form.start_date.data, end_date=form.end_date.data, per_page=form.per_page.data))
            return render_template("show.html", expenses=recent.items, pagination=recent, start_date=form.start_date.data, end_date=form.end_date.data, per_page=form.per_page.data)
    return render_template("query.html", form=form)

@expense_blueprint.route("/show", methods=("GET","POST"))
## def show(pagination=None, start_date=None, end_date=None, page=None, per_page=None):
def show():
    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    recent = Expense.query.filter(Expense.date.between(start_date, end_date)).paginate(page=page,per_page=per_page)
    return render_template("show.html", expenses=recent.items, pagination=recent, start_date=start_date, end_date=end_date, per_page=per_page)

@expense_blueprint.route("/transfer", methods=("GET","POST"))
def transfer():
    if current_user.is_anonymous():
        flash("Please login first!",category="error")
        return redirect(url_for("main.login"))
    form = TransferForm()
    form.source.choices = [(item.id,item.name) for item in Account.query.filter_by(user_id=int(current_user.get_id())).all()]
    form.target.choices = [(item.id,item.name) for item in Account.query.filter_by(user_id=int(current_user.get_id())).all()]
    if form.validate_on_submit():
        transfer = Transfer()
        transfer.source = Account.query.filter(Account.name==form.source.data).first_or_404().id
        transfer.target = Account.query.filter(Account.name==form.target.data).first_or_404().id
        transfer.amount = form.amount.data
        transfer.description = form.description.data
        transfer.date = form.date.data
        transfer.user_id = int(current_user.get_id())
        db.session.add(transfer)
        db.session.commit()
        return redirect(url_for(".home"))
    return render_template("transfer.html", form=form)


