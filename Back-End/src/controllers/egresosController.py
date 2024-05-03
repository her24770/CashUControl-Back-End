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
    egresos = mongo.db.egresos.find({'idUser': ObjectId(id)})
    return Response(json_util.dumps(egresos), mimetype='application/json')

#listar todos los gatos
def allGastos():
    egresos = json_util.dumps(mongo.db.egresos.find())
    return Response(egresos, mimetype='application/json')

#listar por ultimo semestre
def lastSemester():
   # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()

    # Verificar si los datos requeridos están presentes
    if "idUser" not in data or "year" not in data or "semestre" not in data:
        return jsonify({"error": "Faltan parámetros en el cuerpo de la solicitud"}), 400

    id_usuario = data["idUser"]
    year = data["year"]
    semestre = data["semestre"]

    # Calcula la fecha de inicio y fin del semestre
    if semestre == 1:
        fecha_inicio_semestre = datetime(year, 1, 1)
        fecha_fin_semestre = datetime(year, 6, 30)
    elif semestre == 2:
        fecha_inicio_semestre = datetime(year, 7, 1)
        fecha_fin_semestre = datetime(year, 12, 31)
    else:
        return jsonify({"error": "El semestre debe ser 1 o 2"}), 400

    # Consulta los egresos para el usuario en el semestre dado
    egresos = mongo.db.egresos.find({
        "idUser": id_usuario,
        "date": {"$gte": fecha_inicio_semestre, "$lte": fecha_fin_semestre}
    })

    # Convertir los resultados en una lista de diccionarios
    egresos_list = list(egresos)

    return jsonify({"egresos": egresos_list})

