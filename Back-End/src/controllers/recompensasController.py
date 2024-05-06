from flask import request, jsonify, Response
from bson import json_util, ObjectId
from datetime import datetime
from config.validate import dataRequired
from config.mongodb import mongo
import json

def test():
    return jsonify({'message': 'Test recompensas Successfully'})

# Agregar una nueva recompensa
def add_reward():
    data = request.get_json()

    # Validar que los campos requeridos estén presentes
    msg = dataRequired(data, ["id_usuario", "descripcion", "puntos", "fecha_otorgamiento"])
    if msg:
        return msg

    # Convertir id_usuario a ObjectId
    userExist =  mongo.db.users.find_one({'_id': ObjectId(data['id_usuario'])})
    if userExist is None:
        return jsonify({'message': 'El usuario no existe'})

    # Convertir fecha_otorgamiento a formato ISO con datetime
    try:
        data['fecha_otorgamiento'] = datetime.fromisoformat(data['fecha_otorgamiento'])
    except ValueError:
        return jsonify({'message': 'Formato de fecha no válido. Utilice el formato ISO (YYYY-MM-DDTHH:MM:SS)'})

    # Insertar la nueva recompensa en la base de datos
    mongo.db.rewards.insert_one(data)

    return jsonify({'message': 'Recompensa agregada correctamente'})

# Eliminar una recompensa DELETE
def delete_reward(id):
    # Verificar si la recompensa existe
    reward = mongo.db.rewards.find_one({'_id': ObjectId(id)})
    if reward is None:
        return jsonify({'message': 'Recompensa no encontrada'})

    # Eliminar la recompensa de la base de datos
    mongo.db.rewards.delete_one({'_id': ObjectId(id)})

    return jsonify({'message': 'Recompensa eliminada correctamente'})

# Listar todas las recompensas GET
def list_all_rewards():
    rewards = json_util.dumps(mongo.db.rewards.find())
    return Response(rewards, mimetype='application/json')

# Listar recompensas por usuario GET
def list_rewards_by_user(id):
    rewards = json_util.dumps(mongo.db.rewards.find({'id_usuario': ObjectId(id)}))
    return Response(rewards, mimetype='application/json')

# Actualizar una recompensa PUT
def update_reward(id):
    data = request.get_json()

    # Verificar si la recompensa existe
    reward = mongo.db.rewards.find_one({'_id': ObjectId(id)})
    if reward is None:
        return jsonify({'message': 'Recompensa no encontrada'})

    # Actualizar la recompensa en la base de datos
    mongo.db.rewards.update_one({'_id': ObjectId(id)}, {'$set': data})

    return jsonify({'message': 'Recompensa actualizada correctamente'})
