from flask import Blueprint
from controllers.consejosController import *
from config.authenticated import ensureAuth, isAdmin

consejos = Blueprint('consejos', __name__)

consejos.add_url_rule('/test', view_func=test, methods=['GET'])
consejos.add_url_rule('/add', view_func=add_consejos, methods=["POST"])
consejos.add_url_rule('/delete/<id>', view_func=delete_consejo, methods=["DELETE"])
consejos.add_url_rule('/listAll', view_func=list_all_consejos, methods=['GET'])
consejos.add_url_rule('/listByCategoria/<categoria>', view_func=list_ByCategoria, methods=['GET'])
consejos.add_url_rule('/listByUser/<id>', view_func=list_ByUser, methods=['GET'])

##Pa los likes 
consejos.add_url_rule('/like/<id>', view_func=like_consejo, methods=['POST'])
consejos.add_url_rule('/unlike/<id>', view_func=unlike_consejo, methods=['POST'])

## rutas con validacion de token
endpoints_permitidos = ["consejos.get_consejos","consejos.delete_consejos","consejos.list_ByCategoria","consejos.list_ByUser"]

@consejos.before_request
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