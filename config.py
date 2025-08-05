import secrets
import urllib.parse as parse

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Pipoca.26@127.0.0.1:3306/aipo".format(parse.quote("!@R00tP@ssW0rd"))