from flask import Blueprint
from controllers.userController import *
from config.authenticated import ensureAuth, isAdmin

user = Blueprint('users', __name__)

user.add_url_rule('/register', view_func=register, methods=['POST'])
user.add_url_rule('/login', view_func=login, methods=['POST'])
user.add_url_rule('/getAll', view_func=getAll, methods=['GET'])
user.add_url_rule('/getProfile/<id>', view_func=getProfile, methods=['GET'])
user.add_url_rule('/delete/<id>',view_func=delete,methods=['DELETE'])
user.add_url_rule('/update/<id>',view_func=updateProfile,methods=['PUT'])
user.add_url_rule('/updatePassword/<id>',view_func=updatePassword,methods=['PUT'])

## rutas con validacion de token
#endpoints_permitidos = ['users.getAll', 'users.delete', 'users.updateProfile', 'users.getProfile','users.getAll']
endpoints_permitidos = []

@user.before_request
def verify_token_middleware():
    #ensureAtuh
    if request.endpoint in endpoints_permitidos:
        token = request.headers.get('Authorization')
        if not token:
            response = jsonify({"message": "Token no proporcionado"})
            response.status_code = 401
            return response
        return ensureAuth(request.headers.get('Authorization').split(" ")[1], output=False)
    
    #ADMIN
    if request.endpoint == ' ':
        return isAdmin(request.headers.get('Authorization').split(" ")[1], output=False)