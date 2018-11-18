#encoding=utf-8
## from flask import Flask, render_template, Blueprint, redirect, url_for
## from config import DevConfig
## from flask_sqlalchemy import SQLAlchemy
## from sqlalchemy import func
from flask import flash
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, PasswordField, FloatField, BooleanField, SelectField, DateField, IntegerField
from wtforms.validators import optional,DataRequired, Length, EqualTo, URL
from webapp.models import User,Account,candidate_categories
from datetime import datetime,timedelta

## class OpenIDForm(FlaskForm):
##     openid = StringField('OpenID URL', [DataRequired(), URL()])

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember Me")
    duration = SelectField("Duration",choices=[('1', '1 day'),('7', '7 days'),('30', '30 days')])
    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False

        return True

class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=3)])
    confirm = PasswordField('Confirm Password',[DataRequired(), EqualTo('password')])
    ## recaptcha = RecaptchaField()
    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User name already exists')
            return False

        return True

class AccountForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    amount = FloatField("Amount", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])

class UpdateForm(FlaskForm):
    amount = FloatField("Amount", validators=[DataRequired()])

class ExpenseForm(FlaskForm):
    ## category = SelectField("Category",choices=[(item,item) for item in candidate_categories], validators=[DataRequired()])
    category = SelectField("Category", validators=[DataRequired()], coerce=int)
    amount = FloatField("Amount", validators=[DataRequired()])
    ## available_accounts = [(item.id,item.name) for item in Account.query.filter_by(user_id=int(current_user.get_id())).all()]
    ## account = SelectField("Account", choices=available_accounts, validators=[DataRequired()])
    account = SelectField("Account", validators=[DataRequired()], coerce=int)
    pay = BooleanField("Pay?", default=True, validators=[optional()])
    description = StringField("Description", default="")
    date = DateField("Date", default=datetime.now(), validators=[DataRequired()])

class QueryForm(FlaskForm):
    start_date = DateField("Start_date", default=datetime.now()-timedelta(7), validators=[DataRequired()])
    end_date = DateField("End_date", default=datetime.now()+timedelta(1), validators=[optional()])
    per_page = IntegerField("Per_page", default=10, validators=[optional()])

class TransferForm(FlaskForm):
    source = SelectField("Source", validators=[DataRequired()])
    target = SelectField("Target", validators=[DataRequired()])
    amount = FloatField("Amount", validators=[DataRequired()])
    description = StringField("Description", default=u"转账", validators=[DataRequired()])
    date = DateField("Date", default=datetime.now(), validators=[optional()])
    
    ## 验证转账金额是否超过账户内金额数
    ## def validate(self):
    ##     check_validate = super(TransferForm, self).validate()
    ##     if not check_validate:
    ##         return False

        

