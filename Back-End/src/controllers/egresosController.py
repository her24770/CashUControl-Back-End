from flask import request, jsonify, Response
from bson import json_util, ObjectId
from config.validate import *
from config.mongodb import mongo
from datetime import datetime
import json
    
#funcion test
def test():
    return jsonify({'message':'Test egresos Successfully'})

#agregar un egreso 
def addE():
    egresoNew = request.get_json()
    #validar que esten datos requeridos
    msg = dataRequired(egresoNew, ["descripcion", "monto", "date", "idUser"])
    if msg:
        return msg
    #verificar si existe el user
    userExist =  mongo.db.users.find_one({'_id': ObjectId(egresoNew['idUser'])})
    if userExist is None:
        return jsonify({'message': 'El usuario no existe'})
    #actualizar monto
    newEgreso=userExist['activo']+egresoNew['monto']
    mongo.db.users.update_one({'_id': ObjectId(egresoNew['idUser'])},
                              {'$set': {
                                  'activo': newEgreso
                              }})
    #realizar debito
    egresoNew['idUser'] = ObjectId(egresoNew['idUser'])
    egresoNew['date'] = datetime.fromisoformat(egresoNew['date'])
    mongo.db.egresos.insert_one(egresoNew)
    return jsonify({'message': 'Se realizo el debito exitosamente'})

#funcion para buscar por usuario
def searchByUser(id): 
    egresos = mongo.db.egresos.find({'idUser': ObjectId(id)})
    return Response(json_util.dumps(egresos), mimetype='application/json')