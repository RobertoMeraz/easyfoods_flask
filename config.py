import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:@localhost/easyfood')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API
    API_PREFIX = '/api/v1'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-segura')