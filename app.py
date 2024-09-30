import os
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Utilizando variáveis de ambiente para proteger a senha do banco de dados
db_password = os.getenv('DB_PASSWORD')

# Configuração do MongoClient com senha (use variáveis de ambiente para senhas)
client = MongoClient(
    f'mongodb+srv://mjosegabriel13:{db_password}@bigdataclust.isr8i.mongodb.net/?retryWrites=true&w=majority&appName=bigdataclust'
)
db = client['mongodatabase']
colecao = db['bigdataclust']

# Rota para obter todos os itens


@app.route('/items', methods=['GET'])
def get_items():
    items = list(colecao.find())
    for item in items:
        item['_id'] = str(item['_id'])  # Converter ObjectId para string
    return jsonify(items), 200

# Rota para adicionar um novo item


@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    if not new_item or not isinstance(new_item, dict):
        return jsonify({"error": "Dados inválidos"}), 400

    result = colecao.insert_one(new_item)
    new_item['_id'] = str(result.inserted_id)
    return jsonify(new_item), 201

# Rota para atualizar um item


@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    updated_item = request.json
    if not updated_item or not isinstance(updated_item, dict):
        return jsonify({"error": "Dados inválidos"}), 400

    result = colecao.update_one({'_id': ObjectId(id)}, {'$set': updated_item})

    if result.matched_count == 0:
        return jsonify({"error": "Item não encontrado"}), 404

    updated_item['_id'] = id  # Manter o ID no retorno
    return jsonify(updated_item), 200

# Rota para deletar um item


@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    result = colecao.delete_one({'_id': ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Item não encontrado"}), 404

    return jsonify({'result': 'Item deletado'}), 200

# Rota para servir o frontend (HTML)


@app.route('/')
def serve_frontend():
    return render_template('index.html')


if __name__ == '__main__':
    # Certifique-se de definir a variável de ambiente DB_PASSWORD antes de rodar
    if not db_password:
        raise RuntimeError(
            "A variável de ambiente DB_PASSWORD não foi definida.")

    app.run(host='0.0.0.0', port=5000)
