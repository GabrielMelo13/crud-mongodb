import os
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Utilizando variáveis de ambiente para proteger a senha do banco de dados
db_password = os.getenv('DB_PASSWORD')

# Verifica se a variável de ambiente foi definida
if not db_password:
    raise RuntimeError("A variável de ambiente DB_PASSWORD não foi definida.")

# Configuração do MongoClient com a senha
client = MongoClient(
    f'mongodb+srv://mjosegabriel13:{db_password}@bigdataclust.isr8i.mongodb.net/'
)

# Conecta ao banco de dados correto
db = client['bgdatabase']

# Conecta às coleções 'nome' e 'descricao'
nome_collection = db['nome']
descricao_collection = db['descricao']

# Rota para adicionar um novo item nas coleções 'nome' e 'descricao'


@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Dados inválidos"}), 400

    # Verifica se 'nome' e 'descricao' estão presentes no JSON recebido
    if 'nome' in data:
        nome_result = nome_collection.insert_one({'nome': data['nome']})
        data['nome_id'] = str(nome_result.inserted_id)

    if 'descricao' in data:
        descricao_result = descricao_collection.insert_one(
            {'descricao': data['descricao']})
        data['descricao_id'] = str(descricao_result.inserted_id)

    return jsonify(data), 201

# Rota para listar todos os dados das coleções 'nome' e 'descricao'


@app.route('/list_data', methods=['GET'])
def list_data():
    # Lista os dados da coleção 'nome' e 'descricao'
    nomes = list(nome_collection.find())
    descricoes = list(descricao_collection.find())

    # Converte o ObjectId para string
    for nome in nomes:
        nome['_id'] = str(nome['_id'])
    for descricao in descricoes:
        descricao['_id'] = str(descricao['_id'])

    return jsonify({"nomes": nomes, "descricoes": descricoes}), 200

# Rota para remover um item da coleção 'nome' ou 'descricao'


@app.route('/remove_data/<collection>/<id>', methods=['DELETE'])
def remove_data(collection, id):
    if collection == 'nome':
        result = nome_collection.delete_one({'_id': ObjectId(id)})
    elif collection == 'descricao':
        result = descricao_collection.delete_one({'_id': ObjectId(id)})
    else:
        return jsonify({"error": "Coleção inválida"}), 400

    if result.deleted_count == 0:
        return jsonify({"error": "Item não encontrado"}), 404

    return jsonify({'result': 'Item deletado'}), 200

# Rota para servir o frontend (HTML)


@app.route('/')
def serve_frontend():
    return render_template('index.html')


# Inicializa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
