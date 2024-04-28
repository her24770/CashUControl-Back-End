from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from config.mongodb import mongo
from routes.userRoutes import user
from routes.ingresosRoutes import ingresos
from routes.egresosRoutes import egresos
from routes.metasRoutes import metas
from routes.recompensasRoutes import recompensas
from routes.consejosRoutes import consejos

from controllers.userController import initAdmin

config = load_dotenv()

app = Flask(__name__)
# CORS(app, resources={r"*": {"origins": "http://127.0.0.1:3000"}})
CORS(app, origins="http://localhost:3000")

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)


#Rutas
app.register_blueprint(user, url_prefix='/users')
app.register_blueprint(ingresos, url_prefix='/ingresos')
app.register_blueprint(egresos, url_prefix='/egresos')
app.register_blueprint(metas, url_prefix='/metas')
app.register_blueprint(recompensas, url_prefix='/recompensas')
app.register_blueprint(consejos, url_prefix='/consejos')

#funciones
initAdmin()

if __name__ == '__main__':
  app.run(debug=True)