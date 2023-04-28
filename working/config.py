import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP='chipshop.py'
    SECRET_KEY=os.getenv("SECRET_KEY")
    
    
    DEBUG = True
    @staticmethod
    def init_app(app):
        pass
        


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flaskapp"


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flaskapp"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}