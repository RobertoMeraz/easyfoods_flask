from flask import Blueprint
from . import recipes, categories, search, errors

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

api_bp.register_blueprint(recipes.bp)
api_bp.register_blueprint(categories.bp)
api_bp.register_blueprint(search.bp)

# Registrar manejadores de errores
from .errors import register_error_handlers
register_error_handlers(api_bp)