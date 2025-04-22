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

FBKEY = json.loads(os.getenv('CONFIG_FIREBASE')) #pega a variável de ambiente e converte todas as informações no formato JSON

cred = credentials.Certificate(FBKEY)
firebase_admin.initialize_app(cred)

#Conectando com o Firestore da Firebase
db = firestore.client()

#Rota principal de teste
@app.route('/', methods=['GET'])
def index():
    return 'ACADEMIA API ESTÁ ON!! TREINE!'

#Método GET -- Aluno aleatório
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
    
#Método GET -- Listar alunos
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

#Método GET -- Aluno por ID
@app.route('/alunos/<id>', methods=['GET'])
def busca(id):
    doc_ref = db.collection('alunos').document(id) #encontra o endereço do documento que vai se utilizar
    doc = doc_ref.get().to_dict() #pega e abre o documento

    if doc:
        return jsonify(doc), 200
    else:
        return jsonify({'mensagem': 'ERRO! Aluno não encontrado.'}), 404
    
#Método POST -- Adicionar aluno
@app.route('/alunos/', methods=['POST'])
def adicionar_aluno():
    dados = request.json

    if "nome" not in dados or "cpf" not in dados or "status" not in dados:
        return jsonify({'mensagem': 'ERRO! Campos Nome, CPF e Status são obrigatórios.'}), 400
    
    #Contador
    contador_ref = db.collection('controle_id').document('contador')
    contador_doc = contador_ref.get().to_dict()
    ultimo_id = contador_doc.get('id')
    novo_id = int(ultimo_id) + 1
    contador_ref.update({'id': novo_id}) #atualização da correção

    db.collection('alunos').document(str(novo_id)).set({
        "id": novo_id,
        "nome": dados['nome'],
        "cpf": dados['cpf'],
        "status": dados['status']
    }) #set == gravar

    return jsonify({'mensagem': 'Aluno cadastrado com sucesso!'}), 201

#Método PUT -- Alterar matrícula
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

#Método DELETE -- Apagar Aluno
@app.route('/alunos/<id>', methods=['DELETE'])
def excluir_aluno(id):
    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({'mensagem': 'ERRO! Aluno não encontrado.'}), 404
    
    doc_ref.delete()
    return jsonify({'mensagem': 'Aluno excluído com sucesso!'}), 200


if __name__ == '__main__':
    app.run(debug=True)