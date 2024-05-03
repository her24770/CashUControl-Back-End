from flask import Blueprint
from controllers.egresosController import *
from config.authenticated import ensureAuth, isAdmin

egresos = Blueprint('egresos', __name__)

egresos.add_url_rule('/test', view_func=test, methods=['GET'])
egresos.add_url_rule('/searchByUser/<id>', view_func=searchByUser, methods=['GET'])
egresos.add_url_rule('/allEgresos', view_func=allGastos, methods=['GET'])
egresos.add_url_rule('/egresosBySemester/<id>', view_func=lastSemester, methods=['POST'])
egresos.add_url_rule('/egreso', view_func=addE, methods=['POST'])

## rutas con validacion de token
endpoints_permitidos = ['']

@egresos.before_request
def verify_token_middleware():
    token = request.headers.get('Authorization')
    if not token:
        response = jsonify({"message": "Token no proporcionado"})
        response.status_code = 401
        return response
    #ensureAtuh
    if request.endpoint in endpoints_permitidos:
         return ensureAuth(token.split(" ")[1], output=False)
    #ADMIN
    if request.endpoint == ' ':
        return isAdmin(token.split(" ")[1], output=False)