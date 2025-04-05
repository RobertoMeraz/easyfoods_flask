from flask import Blueprint

recipes_bp = Blueprint('recipes', __name__, template_folder='templates')

from app.recipes import routes  # Importa las rutas al final