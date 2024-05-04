from flask import request, jsonify, Response
from bson import json_util, ObjectId
from config.validate import *
from config.mongodb import mongo
import json
    
#funcion listar todos usuarios
def test():
    return jsonify({'message':'Test consejos Successfully'})
def add_consejos():
    data = request.get_json()
    msg = dataRequired(data, ["id_usuario", "descripcion"])
    if msg:
        return msg
    
    mongo.db.consejos.insert_one(data)
    
    return jsonify({'message': 'consejo se añadió correctamente'})

def delete_consejo(id):
    consejo = mongo.db.consejos.find_one({'_id': ObjectId(id)})
    if consejo is None:
        return jsonify({'message': 'consejo no encontrado'})
    
    mongo.db.consejos.delete_one({'_id': ObjectId(id)})
    
    return jsonify({'message': 'consejo eliminado'})

def list_all_consejos():
    consejos = json_util.dumps(mongo.db.consejos.find())
    return Response(consejos, mimetype='application/json')

def update_consejos(id):
    data = request.get_json()

    consejo = mongo.db.consejos.find_one({'_id': ObjectId(id)})
    if consejo is None:
        return jsonify({'message': 'Consejo no encontrado'})

    mongo.db.consejos.update_one({'_id': ObjectId(id)}, {'$set': data})
    
    return jsonify({'message': 'Consejo actualizado correctamente'})
    