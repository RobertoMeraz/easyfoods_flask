from flask import jsonify

def register_error_handlers(bp):
    @bp.errorhandler(400)
    def handle_400(error):
        return bad_request(error.description if hasattr(error, 'description') else 'Solicitud incorrecta')

    @bp.errorhandler(404)
    def handle_404(error):
        return not_found(error.description if hasattr(error, 'description') else 'Recurso no encontrado')

    @bp.errorhandler(500)
    def handle_500(error):
        return error_response(500, 'Error interno del servidor')

def bad_request(message):
    response = jsonify({
        'success': False,
        'error': 'Bad request',
        'message': message
    })
    response.status_code = 400
    return response

def not_found(message):
    response = jsonify({
        'success': False,
        'error': 'Not found',
        'message': message
    })
    response.status_code = 404
    return response

def error_response(status_code, message):
    response = jsonify({
        'success': False,
        'error': 'Error',
        'message': message
    })
    response.status_code = status_code
    return response