from flask import request, jsonify, Response
from bson import json_util, ObjectId
from jwt import encode, decode
from config.validate import *
from config.jwt import create_token
from config.authenticated import userForToken
from config.mongodb import mongo
import json

#funcion para validar logueo
def login():
    data = request.get_json()
    msg = dataRequired(data, ['email', 'password'])
    if msg: 
        return msg
    email = data['email']
    password = data['password']
    user = json.loads(json_util.dumps(mongo.db.users.find_one({'email': email})))
    if user:
        if checkPassword(password, user['password']):
            token = create_token(user)
            return jsonify({ 'user': user,'token':token}) 
    return jsonify({"message": "Credenciales incorrectas"})

#funcion agregar usuario
def register():
    userNew = request.get_json()
    #campos vacios
    msg = dataRequired(userNew, ["email","name","surname","carnet","password"])
    if msg: 
        return msg
    userfind = mongo.db.users.find_one({'email': userNew['email']})
    #encriptar contra
    password=userNew['password']
    userNew['password'] = encrypt(password)
    #no se repita email
    if userfind is None: 
        userNew['role'] = 'USER'
        mongo.db.users.insert_one(userNew)
        return jsonify({'message':'Add succesfully'})
    return jsonify({'message':'Email en uso'})
    
#funcion listar todos usuarios
def getAll():
    users = json_util.dumps(mongo.db.users.find())
    return Response(users, mimetype='application/json')

#funcion buscar perfil por id
def getProfile(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user is None:
        return jsonify({'message':'Usuario no existe'})
    return Response(json_util.dumps(user), mimetype='application/json')

#funcion para actualizar
def updateProfile(id):
    dataUpdate = request.get_json()
    userExist = mongo.db.users.find_one({'_id': ObjectId(id)})
    #vaildacion que el usuario existe en bd
    if userExist is None:
        return jsonify({'message':'Usuario no existe'})
    #validar que el email no se repota en bd
    userEmail = mongo.db.users.find_one({'email': dataUpdate['email']})
    if not userExist['email']== dataUpdate['email']:
        if not userEmail is None:
            return jsonify({'message:':'Email ya esta en uso'})
    #validar permisos de admin y actualizacion de perfil propio para usuario y cambio de rol
    user = userForToken(request.headers['Authorization'].split(" ")[1])
    if not user['role'] == 'ADMIN':
        dataUpdate['role'] = userExist['role']
        if not eval(user['id'])['$oid'] == id:
            return jsonify({'message':'No tiene autorizado hacer esta acción'})
    #actualizar usuario
    mongo.db.users.update_one({'_id': ObjectId(id)},
                                {'$set': {
                                  'email': dataUpdate['email'],
                                  'name': dataUpdate['name'],
                                  'surname': dataUpdate['surname'],
                                  'carnet': dataUpdate['carnet'],
                                  'role': dataUpdate['role']
                            }})
    return jsonify({'message':'Update successfully'})

#funcion para actualizar contraseña
def updatePassword(id):
    dataUpdate = request.get_json()
    userExist = mongo.db.users.find_one({'_id': ObjectId(id)})
    #vaildacion que el usuario existe en bd
    if userExist is None:
        return jsonify({'message':'Usuario no existe'})
    #validar permisos de admin y actualizacion de perfil propio para usuario
    user = userForToken(request.headers['Authorization'].split(" ")[1])
    if not eval(user['id'])['$oid'] == id:
        return jsonify({'message':'No tiene autorizado hacer esta acción'})
    #validar campos vacios
    msg = dataRequired(dataUpdate, ['newPassword', 'password'])
    if msg: 
        return msg
    #validar que sea su contraseña 
    if not checkPassword(dataUpdate['password'], userExist['password']):
        return jsonify({'message': 'Contraseña incorrecta'})
    #actualizar password
    newPassword = encrypt(dataUpdate['newPassword'])
    mongo.db.users.update_one({'_id': ObjectId(id)},
                                {'$set': {'password': newPassword}})
    return jsonify({'message':'Update successfully'})

#funcion para eliminar usuario con validaciones de role y profile      
def delete(id):
    #validar que exista
    userExist = mongo.db.users.find_one({'_id': ObjectId(id)})
    if userExist is None:
        return jsonify({'message':'Usuario no existe'})
    #validar que este autorizado por role y mismo perfil
    user = userForToken(request.headers['Authorization'].split(" ")[1])
    if not user['role'] == 'ADMIN':
        if not eval(user['id'])['$oid'] == id:
            return jsonify({'message':'No tiene autorizado hacer esta acción'})
    #eliminar
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Delete successfully'})

#agregar admin por defecto
def initAdmin():
    userfind = mongo.db.users.find_one({'email': 'ADMIN'})
    if userfind is None:
        password = str(encrypt('123'))
        mongo.db.users.insert_one({
            'email': 'ADMIN', 
            'name': 'ADMIN', 
            'surname': 'DEFAULT', 
            'carnet': 'ADMIN', 
            'password': password, 
            'role': 'ADMIN',
            'activo':0})