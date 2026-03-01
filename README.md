# Compia API

Plataforma de e-commerce para a editora COMPIA, especializada em materiais bibliográficos da área de Inteligência Artificial.

## Sobre o Projeto
Este projeto é uma API RESTful desenvolvida em Django e Django REST Framework para gerenciar produtos e operações de e-commerce da editora COMPIA.

## Tecnologias Utilizadas
- Python 3.11+
- Django 6.0.2
- Django REST Framework
- SQLite3
- drf-spectacular (documentação OpenAPI)

## Requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

## Instalação
1. Clone o repositório:
	```bash
	git clone https://github.com/Projeto-Programacao-Web-I-2025-2/compia-back
	cd compia-back
	```
2. Crie e ative um ambiente virtual:
	```bash
	python3 -m venv venv
	source venv/bin/activate
	```
3. Instale as dependências:
	```bash
	pip install -r requirements.txt
	```

## Como Rodar
1. Execute as migrações do banco de dados:
	```bash
	python manage.py migrate
	```
2. Inicie o servidor de desenvolvimento:
	```bash
	python manage.py runserver
	```

## Estrutura do Projeto
```
compia-back/
├── apps/                 # Aplicativos do projeto
├── compia/               # Configurações do projeto Django
├── db.sqlite3            # Banco de dados SQLite
├── manage.py             # Utilitário de gerenciamento Django
├── requirements.txt      # Dependências do projeto
├── setup.cfg             # Configurações de lint/flake8
└── README.md
```

## Documentação da API
A documentação interativa da API está disponível após rodar o projeto em:
- [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) (Swagger UI)
- [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/) (OpenAPI)
