from flask import request, jsonify, Response
from bson import json_util, ObjectId
from datetime import datetime
from config.validate import *
from config.mongodb import mongo
from config.authenticated import userForToken
    
#funcion test
def test():
    return jsonify({'message':'Test ingresos Successfully'})

#funcion para agregar
def add():
    ingresoNew = request.get_json()
    #validar datos vacios
    msg = dataRequired(ingresoNew, ["descripcion","monto","date","idUser"])
    if msg: 
        return msg
    #validar que exista el usuario
    userExist = mongo.db.users.find_one({'_id': ObjectId(ingresoNew['idUser'])})
    if userExist is None:
        return jsonify({'message':'Usuario no existe'})
    #permiso si es su usuario o rol ADMIN
    # user = userForToken(request.headers['Authorization'].split(" ")[1])
    # if not user['role'] == 'ADMIN':
    #     if not eval(user['id'])['$oid'] == ingresoNew['idUser']:
    #         return jsonify({'message':'No tiene autorizado hacer esta acción'})
    #actualizar monto de usuarios
    newActivo=userExist['activo']+ingresoNew['monto']
    mongo.db.users.update_one({'_id': ObjectId(ingresoNew['idUser'])},
                                {'$set': {
                                  'activo': newActivo
                            }})
    #gagregar
    ingresoNew['idUser'] = ObjectId(ingresoNew['idUser'])
    ingresoNew['date'] =  datetime.fromisoformat(ingresoNew['date'])
    mongo.db.ingresos.insert_one(ingresoNew)
    return jsonify({'message':'Add succesfully'})

def listIdUser(id):
    ingresos = mongo.db.ingresos.find({'idUser': ObjectId(id)})
    return Response(json_util.dumps(ingresos), mimetype='application/json')

def listBySemestre(id):
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
        dateStart = datetime(data['year'], 1, 1)
        dateFinish = datetime(data['year'], 6, 30)
    elif data['semestre']==2:
        dateStart = datetime(data['year'], 7, 1)
        dateFinish = datetime(data['year'], 12, 31)
    else:
        jsonify({'message': 'Semestre invalido'})
    #hacer busqueda entre fechas
    ingresos = mongo.db.ingresos.find({
        'idUser': ObjectId(id),
        'date': {'$gte': dateStart, '$lte': dateFinish}
    })
    return Response(json_util.dumps(ingresos), mimetype='application/json')