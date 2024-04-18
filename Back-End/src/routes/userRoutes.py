from flask import Blueprint
from controllers.userController import *
from config.authenticated import ensureAuth, isAdmin

user = Blueprint('users', __name__)

user.add_url_rule('/register', view_func=register, methods=['POST'])
user.add_url_rule('/login', view_func=login, methods=['POST'])
user.add_url_rule('/getAll', view_func=getAll, methods=['GET'])
user.add_url_rule('/getProfile/<id>', view_func=getProfile, methods=['GET'])
user.add_url_rule('/delete/<id>',view_func=delete,methods=['DELETE'])

## rutas con validacion de token
@user.before_request
def verify_token_middleware():
    #registrados
    if request.endpoint == 'users.getAll' or request.endpoint=='delete':
        return ensureAuth(request.headers['Authorization'].split(" ")[1],output=False)
    
    #ADMIN
    if request.endpoint == 'users.getProfile':
        
        return isAdmin(request.headers['Authorization'].split(" ")[1],output=False)