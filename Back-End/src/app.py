from flask import Flask
from flask_pymongo import PyMongo

app= Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/pythonmongodb'

mongo = PyMongo(app)

@app.route('/users',methods=['POST'])
def create_user():
    return {'mensage':'received'}

if __name__ == '__main__':
    app.run(debug=True)