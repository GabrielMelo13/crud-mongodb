from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
CORS(app)

# Configuração do MongoDB
client = MongoClient('mongodb+srv://mjosegabriel13:<db_password>@bigdataclust.isr8i.mongodb.net/?retryWrites=true&w=majority&appName=bigdataclust')
db = client['mongodatabase']  
colecao = db['bigdataclust']  

@app.route('/items', methods=['GET'])
def get_items():
    items = list(colecao.find())
    for item in items:
        item['_id'] = str(item['_id'])  
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    result = colecao.insert_one(new_item)
    new_item['_id'] = str(result.inserted_id)
    return jsonify(new_item), 201

@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    updated_item = request.json
    colecao.update_one({'_id': ObjectId(id)}, {'$set': updated_item})
    return jsonify(updated_item)

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    colecao.delete_one({'_id': ObjectId(id)})
    return jsonify({'result': 'Item deletado'})

@app.route('/')
def index():
    return "Servidor Flask rodando corretamente!"

@app.route('/')
def serve_frontend():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
