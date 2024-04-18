from jwt import decode, exceptions
from flask import jsonify
from os import getenv

def ensureAuth(token, output=False):
    try: 
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"message": "Token invalido"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token ya espiro"})
        response.status_code = 401
        return response
    

def isAdmin(token,output=False):
    try: 
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        user = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        print(user['role'])
        if not user['role'] == 'ADMIN':
            return jsonify({"message": "NO tiene permisos para esta opcion"})
    except exceptions.DecodeError:
        response = jsonify({"message": "Token invalido"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token ya espiro"})
        response.status_code = 401
        return response
