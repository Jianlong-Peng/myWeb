import os

class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    ## print "os.path.pardir:",os.path.pardir
    ## print "database.db:",os.path.join(os.path.pardir, "database.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.pardir, "database.db")
    ## SQLALCHEMY_DATABASE_URI = "sqlite:///../database.db"
    #sqlite
    #sqlite:///database.db
    #mysql
    #mysql+pymysql://user:password@ip:port/db_name
    #postgres
    #postgresql+psycopg2://user:password@ip:port/db_name
    #mssql
    #mssql+pyodbc://user:password@dsn_name
    #oracle
    #oracle+cx_oracle://user:password@ip:port/db_name
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "2ae6ffe92174935aaefd4b24084ed5ed"

    #for verifyication code of reCAPTCHA
    #developer needs to register in https://www.google.com/recaptcha/intro/index.html
    ## RECAPTCHA_PUBLIC_KEY = ""
    ## RECAPTCHA_PRIVATE_KEY = ""

    DEBUG_TB_INTERCEPT_REDIRECTS = False


