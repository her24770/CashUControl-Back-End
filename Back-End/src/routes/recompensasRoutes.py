from flask import Blueprint
from controllers.recompensasController import *
from config.authenticated import ensureAuth, isAdmin

recompensas = Blueprint('recompensas', __name__)

recompensas.add_url_rule('/test', view_func=test, methods=['GET'])

## rutas con validacion de token
endpoints_permitidos = []

@recompensas.before_request
def verify_token_middleware():
    if request.endpoint in endpoints_permitidos:
         return ensureAuth(request.headers['Authorization'].split(" ")[1],output=False)
    #ADMIN
    if request.endpoint == ' ':
        return isAdmin(request.headers['Authorization'].split(" ")[1],output=False)