import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://apiadmin:password@localhost/schedulerapi_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dziendobry'