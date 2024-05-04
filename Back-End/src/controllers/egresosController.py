from flask import request, jsonify, Response
from bson import json_util, ObjectId
from config.validate import *
from config.mongodb import mongo
from datetime import datetime, timedelta
from config.authenticated import userForToken
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
    #verificar si tiene el saldo necesario
    if userExist['activo'] < egresoNew['monto']:
        return jsonify({'message': 'Fondos insuficientes para realizar la transacción'})
    #actualizar monto
    newEgreso=userExist['activo']-egresoNew['monto']
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
    # Primero, verifica si el usuario existe
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user is None:
        return jsonify({'message':'Usuario no existe'})
    
    # Si el usuario existe, entonces busca los egresos relacionados con ese usuario
    egresos = mongo.db.egresos.find({'idUser': ObjectId(id)})
    return Response(json_util.dumps(egresos), mimetype='application/json')

#listar todos los gatos
def allGastos():
    egresos = json_util.dumps(mongo.db.egresos.find())
    return Response(egresos, mimetype='application/json')

#listar por ultimo semestre
def lastSemester(id):
    data = request.get_json()
    #validar datos vacios
    msg = dataRequired(data, ["year","semestre"])
    if msg: 
        return msg
    #verificar si existe el user
    userExist =  mongo.db.users.find_one({'_id': ObjectId(id)})
    if userExist is None:
        return jsonify({'message': 'El usuario no existe'})
    #establecer rango de fechas para la busqueda
    if data['semestre'] == 1:
        Fincio = datetime(data['year'], 1, 1)
        Ffinal = datetime(data['year'], 6, 30)
    elif data['semestre']==2:
        Fincio = datetime(data['year'], 7, 1)
        Ffinal = datetime(data['year'], 12, 31)
    else:
        jsonify({'message': 'Semestre invalido'})
    #hacer busqueda entre fechas
    ingresos = mongo.db.ingresos.find({
        'idUser': ObjectId(id),
        'date': {'$gte': Fincio, '$lte': Ffinal}
    })
    return Response(json_util.dumps(ingresos), mimetype='application/json')
