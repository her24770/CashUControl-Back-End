from flask import request, jsonify, Response
from bson import json_util, ObjectId
from datetime import datetime
from config.validate import *
from config.mongodb import mongo
from config.authenticated import userForToken
    
#funcion listar todos usuarios
def test():
    return jsonify({'message':'Test metas Successfully'})

def add():
    metaNew = request.get_json()
    #validar datos vacios   
    msg = dataRequired(metaNew, ["idUser", "tipo","monto","dateObjetivo"])
    if msg: 
        return msg
    #validar que exista el usuario
    userExist = mongo.db.users.find_one({'_id': ObjectId(metaNew['idUser'])})
    if userExist is None:
        return jsonify({'message':'Usuario no existe'})
    #permiso si es su usuario o rol ADMIN
    # user = userForToken(request.headers['Authorization'].split(" ")[1])
    # if not user['role'] == 'ADMIN':
    #     if not eval(user['id'])['$oid'] == metaNew['idUser']:
    #         return jsonify({'message':'No tiene autorizado hacer esta acción'})   
    #gagregar
    metaNew['idUser'] = ObjectId(metaNew['idUser'])
    metaNew['dateObjetivo'] =  datetime.fromisoformat(metaNew['dateObjetivo'])
    metaNew['dateCreacion'] =  datetime.now()
    mongo.db.metas.insert_one(metaNew)
    return jsonify({'message':'Add succesfully'})

def edit(idMeta):
    metaNew = request.get_json()
    #validar datos vacios   
    msg = dataRequired(metaNew, ["tipo","monto","dateObjetivo"])
    if msg: 
        return msg 
    #validar que exista el usuario
    metaExist = mongo.db.metas.find_one({'_id': ObjectId(idMeta)})
    if metaExist is None:
        return jsonify({'message':'Meta no existe'})
    #permiso si es su usuario o rol ADMIN
    # user = userForToken(request.headers['Authorization'].split(" ")[1])
    # if not user['role'] == 'ADMIN':
    #     if not eval(user['id'])['$oid'] == metaNew['idUser']:
    #         return jsonify({'message':'No tiene autorizado hacer esta acción'})    
    #editar
    res = mongo.db.metas.update_one({'_id': ObjectId(idMeta)},
                                {'$set': {
                                  'tipo': metaNew['tipo'],
                                  'monto': metaNew['monto'],
                                  'dateObjetivo': datetime.fromisoformat(metaNew['dateObjetivo'])
                            }})
    return jsonify({'message':'edit succesfully'})

def listIdUser(id):
    #validar que exista el usuario
    userExist = mongo.db.users.find_one({'_id': ObjectId(id)})
    if userExist is None:
        return jsonify({'message':'Usuario no existe'})
    #permiso si es su usuario o rol ADMIN
    # user = userForToken(request.headers['Authorization'].split(" ")[1])
    # if not user['role'] == 'ADMIN':
    #     if not eval(user['id'])['$oid'] == id:
    #         return jsonify({'message':'No tiene autorizado hacer esta acción'})
    # listar las metas por usuario
    metas = mongo.db.metas.find({'idUser': ObjectId(id)})
    return Response(json_util.dumps(metas), mimetype='application/json')

def findId(idMeta):
    #validar que exista el usuario
    meta = mongo.db.metas.find_one({'_id': ObjectId(idMeta)})
    if meta is None:
        return jsonify({'message':'meta no existe'})
    #permiso si es su usuario o rol ADMIN
    # user = userForToken(request.headers['Authorization'].split(" ")[1])
    # if not user['role'] == 'ADMIN':
    #     if not eval(user['id'])['$oid'] == id:
    #         return jsonify({'message':'No tiene autorizado hacer esta acción'})
        
    return Response(json_util.dumps(meta), mimetype='application/json')

def deleted(id):
    # Verificar si la recompensa existe
    reward = mongo.db.metas.find_one({'_id': ObjectId(id)})
    if reward is None:
        return jsonify({'message': 'Meta no encontrada'})

    # Eliminar la recompensa de la base de datos
    mongo.db.metas.delete_one({'_id': ObjectId(id)})

    return jsonify({'message': 'Meta eliminada correctamente'})
