from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from config.mongodb import mongo
from routes.userRoutes import user
from controllers.userController import initAdmin

config = load_dotenv()

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)


#Rutas
app.register_blueprint(user, url_prefix='/users')

#funciones
initAdmin()

if __name__ == '__main__':
  app.run(debug=True)