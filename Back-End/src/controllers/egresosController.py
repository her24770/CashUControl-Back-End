from flask import request, jsonify, Response
from bson import json_util, ObjectId
from config.validate import *
from config.mongodb import mongo
import json
    
#funcion listar todos usuarios
def test():
    return jsonify({'message':'Test egresos Successfully'})