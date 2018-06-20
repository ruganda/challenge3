import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = os.getenv('SECRET') or "secret"
    DB = 'ride_db'


class DevelopmentConfiguration(Config):
    """Configurations for Development."""
    DEBUG = True
    DB = 'ride_db'

class TestingConfiguration(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DB = 'test_db'

class ProductionConfiguration(Config):
    """Configurations for Production."""
    DEBUG = False

configuration = {
    'DEFAULT': DevelopmentConfiguration,
    'TESTING': TestingConfiguration,
    'DEVELOPMENT': DevelopmentConfiguration,
    'PRODUCTION': ProductionConfiguration
}
