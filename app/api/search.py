from flask import Blueprint, jsonify, request
from app.models import Receta
from .errors import bad_request, error_response

bp = Blueprint('search_api', __name__, url_prefix='/search')

@bp.route('/', methods=['GET'])
def search_recipes():
    try:
        query = request.args.get('q', '').strip()
        if len(query) < 2:
            return bad_request('La búsqueda debe tener al menos 2 caracteres')
        
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        pagination = Receta.query.filter(
            (Receta.titulo.ilike(f'%{query}%')) | 
            (Receta.descripcion.ilike(f'%{query}%'))
        ).paginate(page=page, per_page=per_page)
        
        recipes = [receta.to_dict() for receta in pagination.items]
        
        return jsonify({
            'success': True,
            'data': recipes,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'query': query
        })
    except Exception as e:
        return error_response(500, str(e))