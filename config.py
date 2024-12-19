class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///stocks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'not_a_real_key'