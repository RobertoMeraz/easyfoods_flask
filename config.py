from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

class Config:
    # Configuración esencial
    SECRET_KEY = os.getenv('SECRET_KEY', 'una_clave_secreta_por_defecto')
    
    # Configuración de MySQL (versión lista para usar)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 
        'mysql+pymysql://root:easy54321.0@localhost:3306/easyfoods')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 299,
        'pool_pre_ping': True
    }

    # Configuración adicional para MySQL 8.0+
    SQLALCHEMY_POOL_RECYCLE = 299  # Para evitar timeout de conexión