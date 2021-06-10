from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'db'
app.config['MONGO_URI'] = 'mongodb://localhost:10533/db'
mongo = PyMongo(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    users = mongo.db.users
    output = []
    for user in users.find_all():
        output.append({'name' : user['name'], 'age' : user['age'], 'languages' : user['languages']})
    user = users.find_one({'name':name})
    return jsonify({'result': output})

@app.route('/users/<name>', methods=['GET'])
def get_one_user(name):
    users = mongo.db.users
    user = users.find_one({'name':name})
    if user:
        output = {'name' : user['name'], 'age' : user['age'], 'languages' : user['languages']}
    else:
        output = "No user exist"
    return jsonify({'result': output})

@app.route('/users', methods=['POST'])
def add_user():
  user = mongo.db.users
  name = request.json['name']
  age = request.json['age']
  languages = request.json['languages']
  user_id = user.insert({'name' : name, 'age' : age, 'languages' : languages})
  new_user = user.find_one({'_id': user_id })
  output = {'name' : new_user['name'], 'age' : new_user['age'], 'languages': new_user['languages']}
  return jsonify({'result' : output})

if __name__ == "__main__":
    app.run(debug=True)
