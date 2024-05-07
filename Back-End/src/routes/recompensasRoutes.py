from flask import Blueprint
from controllers.recompensasController import *
from config.authenticated import ensureAuth, isAdmin

recompensas = Blueprint('recompensas', __name__)

recompensas.add_url_rule('/test', view_func=test, methods=['GET'])
recompensas.add_url_rule('/agregar',view_func=add_reward, methods=['POST'])
recompensas.add_url_rule('/eliminar/<id>',view_func=delete_reward, methods=['DELETE'])
# recompensas.add_url_rule('/update/<id>',view_func=update_reward,methods=['PUT'])
recompensas.add_url_rule('/listare/<id>',view_func=list_rewards_by_user,methods=['GET'])
recompensas.add_url_rule('/lis',view_func=list_all_rewards,methods=['GET'])

## rutas con validacion de token
#endpoints_permitidos = ['recompensas.add_reward','recompensas.delete_reward','recompensas.update_reward','recompensas.list_rewards_by_user','recompensas.list_all_rewards']
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