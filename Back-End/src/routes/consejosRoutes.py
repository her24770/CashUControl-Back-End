from flask import Blueprint
from controllers.consejosController import *
from config.authenticated import ensureAuth, isAdmin

consejos = Blueprint('consejos', __name__)

consejos.add_url_rule('/test', view_func=test, methods=['GET'])

## rutas con validacion de token
endpoints_permitidos = []

@consejos.before_request
def verify_token_middleware():
    if request.endpoint in endpoints_permitidos:
         return ensureAuth(request.headers['Authorization'].split(" ")[1],output=False)
    #ADMIN
    if request.endpoint == ' ':
        return isAdmin(request.headers['Authorization'].split(" ")[1],output=False)