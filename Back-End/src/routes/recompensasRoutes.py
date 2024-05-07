from flask import Blueprint
from controllers.recompensasController import *
from config.authenticated import ensureAuth, isAdmin

recompensas = Blueprint('recompensas', __name__)

recompensas.add_url_rule('/test', view_func=test, methods=['GET'])

## rutas con validacion de token
#endpoints_permitidos = []
endpoints_permitidos = []

@recompensas.before_request
def verify_token_middleware():
    #ensureAtuh
    if request.endpoint in endpoints_permitidos:
        token = request.headers.get('Authorization')
        if not token:
            response = jsonify({"message": "Token no proporcionado"})
            response.status_code = 401
            return response
        return ensureAuth(token.split(" ")[1], output=False)
    #ADMIN
    if request.endpoint == ' ':
        return isAdmin(token.split(" ")[1], output=False)