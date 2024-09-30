from flask import Flask, jsonify, request, send_from_directory, render_template
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuração do MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/crud_db"
mongo = PyMongo(app)

# Configuração do MongoClient com senha
client = MongoClient(
    'mongodb+srv://mjosegabriel13:<db_password>@bigdataclust.isr8i.mongodb.net/?retryWrites=true&w=majority&appName=bigdataclust'
)
db = client['mongodatabase']
colecao = db['bigdataclust']

# Rota para obter todos os itens


@app.route('/items', methods=['GET'])
def get_items():
    items = list(colecao.find())
    for item in items:
        item['_id'] = str(item['_id'])  # Converter ObjectId para string
    return jsonify(items)

# Rota para adicionar um novo item


@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    result = colecao.insert_one(new_item)
    new_item['_id'] = str(result.inserted_id)
    return jsonify(new_item), 201

# Rota para atualizar um item


@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    updated_item = request.json
    colecao.update_one({'_id': ObjectId(id)}, {'$set': updated_item})
    return jsonify(updated_item)

# Rota para deletar um item


@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    colecao.delete_one({'_id': ObjectId(id)})
    return jsonify({'result': 'Item deletado'})

# Rota para servir o frontend (HTML)


@app.route('/')
def serve_frontend():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
