from flask import request, jsonify, Response
from bson import json_util, ObjectId
from datetime import datetime
from config.validate import *
from config.mongodb import mongo
import json
    
#funcion listar todos usuarios
def test():
    return jsonify({'message':'Test consejos Successfully'})

def add_consejos():
    data = request.get_json()
    #mensajes vacios
    msg = dataRequired(data, ["id_usuario", "descripcion","fecha"])
    if msg:
        return msg
    #buscar que el usuario exista
    userExist = mongo.db.users.find_one({'_id': ObjectId(data['id_usuario'])})
    if userExist is None:
        return jsonify({'message':'Usuario no existe'})
    #agregar
    data['id_usuario']=ObjectId(data['id_usuario'])
    data['fecha']= datetime.fromisoformat(data['fecha'])
    mongo.db.consejos.insert_one(data)
    return jsonify({'message': 'Add successfully'})

def delete_consejo(id):
    consejo = mongo.db.consejos.find_one({'_id': ObjectId(id)})
    if consejo is None:
        return jsonify({'message': 'consejo no encontrado'})
    mongo.db.consejos.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'delete successfully'})


def list_all_consejos():
    consejos = json_util.dumps(mongo.db.consejos.find())
    return Response(consejos, mimetype='application/json')

def list_ByCategoria(categoria):
    consejos = mongo.db.consejos.find({'categoria':categoria})
    return Response(json_util.dumps(consejos), mimetype='application/json')

def list_ByUser(id):
    #buscar que el usuario exista
    userExist = mongo.db.users.find_one({'_id': ObjectId(id)})
    if userExist is None:
        return jsonify({'message':'Usuario no existe'})
    #buscar
    consejos = mongo.db.consejos.find({"id_usuario": ObjectId(id)})
    return Response(json_util.dumps(consejos), mimetype='application/json')


"""    Fucion pendiente de usar
def update_consejos(id):
    data = request.get_json()

    consejo = mongo.db.consejos.find_one({'_id': ObjectId(id)})
    if consejo is None:
        return jsonify({'message': 'Consejo no encontrado'})

    mongo.db.consejos.update_one({'_id': ObjectId(id)}, {'$set': data})
    
    return jsonify({'message': 'Consejo actualizado correctamente'})
"""