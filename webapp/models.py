#encoding=utf-8
## from flask import Flask, render_template, Blueprint, redirect, url_for
## from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin
from sqlalchemy.orm.exc import NoResultFound
## from sqlalchemy import func
## from flask_wtf import Form
## from wtforms import StringField, TextAreaField
## from wtforms.validators import DataRequired, Length
## import datetime
from extensions import bcrypt

db = SQLAlchemy()
#one can use db.create_all() to create the table

'''
db.String   --> varchar
db.Text     --> text
db.Integer
db.Float
db.Boolean
db.Date
db.DateTime
db.Time
'''

categories = db.Table("expense_category",
    db.Column('expense_id', db.Integer, db.ForeignKey('expense.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class User(db.Model):
    ## by defualt, the class name in lower case will be table name.
    ## __tablename__ == 'user_table_name'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    accounts = db.relationship(
        'Account',
        backref = 'user',
        lazy = 'dynamic'
    )
    #about lazy
    #1) subquery: it will load all relation objects once Post is loaded
    #2) dynamic: all relation objects will be loaded only when it's called/used.

    #it's not necessary
    #by default, SQLALchemy will automatically create __init__, and all attributes will be parameters
    def __init__(self, username):
        self.username = username
    
    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return unicode(self.id)

class Account(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    founds = db.relationship(
        'Found',
        backref = 'account',
        lazy = 'dynamic'
    )
    #latest amount
    amount = db.Column(db.Float())
    description = db.Column(db.Text())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    date = db.Column(db.DateTime())

    def __repr__(self):
        return "<Account '{0}', Amount '{1}', Description '{2}'>".format(self.name, self.amount, self.description)

#记录历史金额
class Found(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    account_id = db.Column(db.Integer(), db.ForeignKey('account.id'))
    amount = db.Column(db.Float())
    date = db.Column(db.DateTime())
    description = db.Column(db.String())

    def __repr__(self):
        return "<The Account '{0}' has {1} Yuan at {2}".format(self.get_account_name(), self.amount, self.date)

    def get_account_name(self):
        if self.account_id is None: return "N/A"
        else:
            a = Account.query.get(self.account_id)
            if a is None: return "N/A"
            else: return a.name


candidate_categories = [u"伙食",u"零食",u"衣服",u"交通",u"房租",u"水电煤气",u"房贷",u"装修",u"医疗",u"购房",u"物业",u"其它"]

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(255))

    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return u"<Expense Category '{}'".format(self.category)


class Expense(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Float())
    account_id = db.Column(db.Integer(), db.ForeignKey('account.id'))
    category_id = db.Column(db.Integer(), db.ForeignKey("category.id"))
    description = db.Column(db.Text())
    date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    pay = db.Column(db.Boolean())

    def __repr__(self):
        return "<Category '{0}', Amount '{1}', Account '{2}', Description '{3}', Date '{4}'".format(self.get_category_name(), self.amount, self.get_account_name(), self.description, self.date)

    def get_account_name(self):
        if self.account_id is None: return "N/A"
        else:
            a = Account.query.get(self.account_id)
            if a is None: return "N/A"
            else: return a.name

    def get_category_name(self):
        if self.category_id is None: return "N/A"
        else:
            a = Category.query.get(self.category_id)
            if a is None: return "N/A"
            else: return a.category

    def get_user_name(self):
        if self.user_id is None: return "N/A"
        else:
            a = User.query.get(self.user_id)
            if a is None: return "N/A"
            else: return a.username
    

class Transfer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    source = db.Column(db.Integer(), db.ForeignKey('account.id'))
    target = db.Column(db.Integer(), db.ForeignKey('account.id'))
    amount = db.Column(db.Float())
    description = db.Column(db.String())
    date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Transfer {0} from {1} to {2} at {3} by {4}>".format(self.amount, self.get_account_name(self.source), self.get_account_name(self.target), self.date, self.get_user_name())

    def get_account_name(self, account_id):
        if account_id is None: return "N/A"
        else:
            a = Account.query.get(account_id)
            if a is None: return "N/A"
            else: return a.name

    def get_user_name(self):
        if self.user_id is None: return "N/A"
        else:
            a = User.query.get(self.user_id)
            if a is None: return "N/A"
            else: return a.username

