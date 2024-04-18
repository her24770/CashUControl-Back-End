from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from config.mongodb import mongo
from routes.userRoutes import user

config = load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)

app.register_blueprint(user, url_prefix='/users')

if __name__ == '__main__':
  app.run(debug=True)