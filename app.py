from flask import Flask, jsonify, request
import random
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

FBKEY = json.loads(os.getenv('CONFIG_FIREBASE'))
cred = credentials.Certificate(FBKEY)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Rota principal de teste
@app.route('/', methods=['GET'])
def index():
    return 'ACADEMIA API ESTÁ ON!! TREINE!'

# ROTAS ALUNOS

# Método GET -- Aluno aleatório
@app.route('/alunos', methods=['GET'])
def aluno_aleatorio():
    alunos = []
    lista = db.collection('alunos').stream()
    for item in lista:
        alunos.append(item.to_dict())

    if alunos:
        return jsonify(random.choice(alunos)), 200
    else:
        return jsonify({'mensagem': 'ERRO! Nenhum aluno encontrado.'}), 404

# Método GET -- Listar todos alunos
@app.route('/alunos/lista', methods=['GET'])
def aluno_lista():
    alunos = []
    lista = db.collection('alunos').stream()

    for item in lista:
        alunos.append(item.to_dict())

    if alunos:
        return jsonify(alunos), 200
    else:
        return jsonify({'mensagem': 'ERRO! Nenhum aluno encontrado.'}), 404

# Método GET -- Buscar aluno por ID
@app.route('/alunos/<id>', methods=['GET'])
def busca(id):
    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get().to_dict()

    if doc:
        return jsonify(doc), 200
    else:
        return jsonify({'mensagem': 'ERRO! Aluno não encontrado.'}), 404

# Método POST -- Adicionar novo aluno
@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    dados = request.json

    if "nome" not in dados or "cpf" not in dados or "status" not in dados:
        return jsonify({'mensagem': 'ERRO! Campos Nome, CPF e Status são obrigatórios.'}), 400

    contador_ref = db.collection('controle_id').document('contador')
    contador_doc = contador_ref.get().to_dict()
    ultimo_id = contador_doc.get('id')
    novo_id = int(ultimo_id) + 1
    contador_ref.update({'id': novo_id})

    db.collection('alunos').document(str(novo_id)).set({
        "id": novo_id,
        "nome": dados['nome'],
        "cpf": dados['cpf'],
        "status": dados['status']
    })

    return jsonify({'mensagem': 'Aluno cadastrado com sucesso!'}), 201

# Método PUT -- Atualizar aluno
@app.route('/alunos/<id>', methods=['PUT'])
def alterar_aluno(id):
    dados = request.json

    if "nome" not in dados or "cpf" not in dados or "status" not in dados:
        return jsonify({'mensagem': 'ERRO! Campos Nome, CPF e Status são obrigatórios.'}), 400

    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.update({
            "nome": dados['nome'],
            "cpf": dados['cpf'],
            "status": dados['status']
        })
        return jsonify({'mensagem': 'Matrícula atualizada com sucesso!'}), 201
    else:
        return jsonify({'mensagem': 'ERRO! Matrícula não encontrada.'}), 404

# Método DELETE -- Excluir aluno
@app.route('/alunos/<id>', methods=['DELETE'])
def excluir_aluno(id):
    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({'mensagem': 'ERRO! Aluno não encontrado.'}), 404

    doc_ref.delete()
    return jsonify({'mensagem': 'Aluno excluído com sucesso!'}), 200

# -----------------------------------------------
# ROTAS TREINOS (ADICIONADA)

# Método GET -- Listar treinos inferiores
@app.route('/inferior/lista', methods=['GET'])
def listar_inferior():
    treinos_inferior = []
    lista = db.collection('inferior').stream()

    for item in lista:
        treino = item.to_dict()
        treino['id'] = item.id
        treinos_inferior.append(treino)

    if treinos_inferior:
        return jsonify(treinos_inferior), 200
    else:
        return jsonify({'mensagem': 'ERRO! Nenhum treino inferior encontrado.'}), 404

# Método GET -- Listar treinos superiores
@app.route('/superior/lista', methods=['GET'])
def listar_superior():
    treinos_superior = []
    lista = db.collection('superior').stream()

    for item in lista:
        treino = item.to_dict()
        treino['id'] = item.id
        treinos_superior.append(treino)

    if treinos_superior:
        return jsonify(treinos_superior), 200
    else:
        return jsonify({'mensagem': 'ERRO! Nenhum treino superior encontrado.'}), 404

# Método POST -- Cadastrar treino para um aluno
@app.route('/alunos/<id>/treinos', methods=['POST'])
def cadastrar_treino(id):
    dados = request.json

    if not dados or 'exercicios' not in dados:
        return jsonify({'mensagem': 'ERRO! Informações de treino incompletas.'}), 400

    try:
        treino_ref = db.collection('alunos').document(id).collection('treinos').document()
        treino_ref.set({
            'exercicios': dados['exercicios'],
            'dataCriacao': firestore.SERVER_TIMESTAMP
        })

        return jsonify({'mensagem': 'Treino cadastrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao cadastrar treino: {str(e)}'}), 500

# Método GET - Listar todos os treinos de um aluno específico
@app.route('/alunos/<id>/treinos', methods=['GET'])
def listar_treinos_aluno(id):
    try:
        treinos = []
        treinos_ref = db.collection('alunos').document(id).collection('treinos').stream()

        for treino in treinos_ref:
            t = treino.to_dict()
            t['id'] = treino.id
            treinos.append(t)

        return jsonify(treinos), 200
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao buscar treinos: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
