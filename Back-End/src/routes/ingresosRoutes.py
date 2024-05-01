from flask import Blueprint
from controllers.ingresosController import *
from config.authenticated import ensureAuth, isAdmin

ingresos = Blueprint('ingresos', __name__)

ingresos.add_url_rule('/test', view_func=test, methods=['GET'])
ingresos.add_url_rule('/listIdUser/<id>', view_func=listIdUser, methods=['GET'])
ingresos.add_url_rule('/listSemestre/<id>', view_func=listBySemestre,methods=['POST'])
ingresos.add_url_rule('/add', view_func=add, methods=['POST'])

## rutas con validacion de token
endpoints_permitidos = ['ingresos.add','ingresos.listIdUser','ingresos.listBySemestre']

@ingresos.before_request
def verify_token_middleware():
    if request.endpoint in endpoints_permitidos:
         return ensureAuth(request.headers['Authorization'].split(" ")[1],output=False)
    #ADMIN
    if request.endpoint == ' ':
        return isAdmin(request.headers['Authorization'].split(" ")[1],output=False)