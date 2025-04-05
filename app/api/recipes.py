from flask import Blueprint, jsonify, request
from app.models import Receta
from .errors import bad_request, not_found, error_response

bp = Blueprint('recipes_api', __name__, url_prefix='/recipes')

@bp.route('/', methods=['GET'])
def get_recipes():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        pagination = Receta.query.paginate(page=page, per_page=per_page)
        recipes = [receta.to_dict() for receta in pagination.items]
        
        return jsonify({
            'success': True,
            'data': recipes,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        })
    except Exception as e:
        return error_response(500, str(e))

@bp.route('/<int:id>', methods=['GET'])
def get_recipe(id):
    try:
        recipe = Receta.query.get(id)
        if recipe is None:
            return not_found('Receta no encontrada')
        return jsonify({
            'success': True,
            'data': recipe.to_dict()
        })
    except Exception as e:
        return error_response(500, str(e))

@bp.route('/random', methods=['GET'])
def get_random_recipe():
    try:
        recipe = Receta.query.order_by(db.func.random()).first()
        if recipe is None:
            return not_found('No hay recetas disponibles')
        return jsonify({
            'success': True,
            'data': recipe.to_dict()
        })
    except Exception as e:
        return error_response(500, str(e))