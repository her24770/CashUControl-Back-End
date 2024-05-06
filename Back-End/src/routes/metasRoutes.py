from flask import Blueprint
from controllers.metasController import *
from config.authenticated import ensureAuth, isAdmin

metas = Blueprint('metas', __name__)

metas.add_url_rule('/test', view_func=test, methods=['GET'])
metas.add_url_rule('/add', view_func=add, methods=['POST'])
metas.add_url_rule('/listIdUser/<id>', view_func=listIdUser, methods=['GET'])
metas.add_url_rule('/edit/<idMeta>', view_func=edit, methods=['PUT'])
metas.add_url_rule('/findId/<idMeta>', view_func=findId, methods=['GET'])

## rutas con validacion de token
endpoints_permitidos = ['metas.add','metas.listIdUser','metas.edit','metas.findId']
#endpoints_permitidos = []

@metas.before_request
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