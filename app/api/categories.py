from flask import Blueprint, jsonify
from app.models import Categoria, Receta
from .errors import not_found, error_response

bp = Blueprint('categories_api', __name__, url_prefix='/categories')

@bp.route('/', methods=['GET'])
def get_categories():
    try:
        categories = Categoria.get_all_for_api()
        return jsonify({
            'success': True,
            'data': categories,
            'count': len(categories)
        })
    except Exception as e:
        return error_response(500, str(e))

@bp.route('/<slug>', methods=['GET'])
def get_category(slug):
    try:
        category = Categoria.query.filter_by(slug=slug).first()
        if category is None:
            return not_found('Categoría no encontrada')
        return jsonify({
            'success': True,
            'data': category.to_dict()
        })
    except Exception as e:
        return error_response(500, str(e))

@bp.route('/<slug>/recipes', methods=['GET'])
def get_recipes_by_category(slug):
    try:
        category = Categoria.query.filter_by(slug=slug).first()
        if category is None:
            return not_found('Categoría no encontrada')
            
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        pagination = Receta.query.filter_by(categoria_id=category.id).paginate(
            page=page, per_page=per_page)
        recipes = [receta.to_dict() for receta in pagination.items]
        
        return jsonify({
            'success': True,
            'data': recipes,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'category': category.to_dict()
        })
    except Exception as e:
        return error_response(500, str(e))