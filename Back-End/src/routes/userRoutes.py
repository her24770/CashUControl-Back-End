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
#endpoints_permitidos = ['users.getAll', 'users.delete', 'users.updateProfile', 'users']
endpoints_permitidos = []
@user.before_request
def verify_token_middleware():
    if request.endpoint in endpoints_permitidos:
         print("hola")
         print(request.headers['Authorization'])
         return ensureAuth(request.headers['Authorization'].split(" ")[1],output=False)
    #ADMIN
    if request.endpoint == 'users.jijija':
        return isAdmin(request.headers['Authorization'].split(" ")[1],output=False)