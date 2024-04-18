from flask import request, jsonify, Response
from bson import json_util, ObjectId
from jwt import encode, decode
from config.validate import *
from config.jwt import create_token
from config.mongodb import mongo
import json

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
    response = jsonify({"message": "Credenciales incorrectas"})
    return response

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
    

def getAll():
    users = json_util.dumps(mongo.db.users.find())
    return Response(users, mimetype='application/json')

def getProfile(id):
    user = json_util.dumps(mongo.db.users.find_one({'_id': ObjectId(id)}))
    return Response(user, mimetype='application/json')


def delete(id):
    response = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if response.deleted_count >= 1:
        return 'User deleted successfully', 200
    else:
        return 'User not found', 404
    
#deleteÑrofile, updateProfile, initAdmin, update,delete