import bcrypt
from flask import jsonify

#encripta contraseña
def encrypt(password):
    try:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except Exception as err:
        print(err)
        return err

#compara encriptacion con password plana
def checkPassword(password, hash):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
    except Exception as err:
        print(err)
        return False
    
#funcion para espacion vacios
def dataRequired(data, required_keys):
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        missing_keys_str = ', '.join(missing_keys)
        message = f"{missing_keys_str} requeridos para completar el proceso"
        return jsonify({"message": message}), 400
    return None