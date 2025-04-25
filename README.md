# 🏋️‍♀️ API - Sistema de Academia

API RESTful desenvolvida em Flask para gerenciar dados de alunos de uma academia, utilizando Firebase Firestore como banco de dados. Hospedada facilmente com Vercel para testes e demonstrações.

---

## 🚀 Tecnologias Utilizadas

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
[![Lucide](https://img.shields.io/badge/Lucide%20Icons-000000?style=for-the-badge&logo=lucide&logoColor=white)]()

---

## 📦 Funcionalidades

- ✅ Buscar um aluno aleatório
- 📋 Listar todos os alunos
- 🔍 Consultar aluno por ID
- ➕ Cadastrar um novo aluno
- ✏️ Atualizar matrícula do aluno
- ❌ Excluir aluno do sistema

---

## 📁 Estrutura Básica

```
/
├── app.py               # Código principal da API
├── .env                 # Variáveis de ambiente (Firebase)
├── requirements.txt     # Dependências do projeto
├── vercel.json          # Configuração de deploy (opcional)
```

---

## 🌍 Teste o Projeto Online  

Você pode testar a aplicação diretamente na Vercel clicando no botão abaixo:  

[![Testar na Vercel](https://img.shields.io/badge/Testar%20na%20Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://aplica-o-2-api-bd.vercel.app/)  

Se o botão não funcionar, copie e cole o seguinte link no seu navegador:  

🔗 **[Acesse o projeto aqui](https://aplica-o-2-api-bd.vercel.app/)**  

---

| Método | Endpoint             | Descrição                          |
|--------|----------------------|------------------------------------|
| GET    | `/`                  | Teste: retorna mensagem da API     |
| GET    | `/alunos`            | Retorna um aluno aleatório         |
| GET    | `/alunos/lista`      | Lista todos os alunos              |
| GET    | `/alunos/<id>`       | Consulta aluno por ID              |
| POST   | `/alunos/`           | Adiciona um novo aluno             |
| PUT    | `/alunos/<id>`       | Atualiza dados do aluno            |
| DELETE | `/alunos/<id>`       | Remove o aluno                     |

---

## 👨‍💻👩🏻‍💻 Projeto desenvolvido por

**Igor Gabriel e Lígia Costa**  
Curso Técnico em Análise e Desenvolvimento de Sistemas -- SENAI - 2025

---

## 📄 Licença

Este projeto está sob a licença MIT.