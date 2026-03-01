# Compia API

Plataforma de e-commerce para a editora COMPIA, especializada em materiais bibliográficos da área de Inteligência Artificial.

## Índice
- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Requisitos](#requisitos)
- [Instalação](#instalacao)
- [Como Rodar](#como-rodar)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Documentação da API](#documentacao-da-api)
- [Contribuição](#contribuicao)
- [Licença](#licenca)

## Sobre o Projeto
Este projeto é uma API RESTful desenvolvida em Django e Django REST Framework para gerenciar produtos e operações de e-commerce da editora COMPIA.

## Tecnologias Utilizadas
- Python 3.11+
- Django 6.0.2
- Django REST Framework
- SQLite3 (padrão, pode ser alterado para outros bancos)
- drf-spectacular (documentação OpenAPI)
- django-jazzmin (admin customizado)

## Requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

## Instalação
1. Clone o repositório:
	```bash
	git clone <url-do-repositorio>
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
- [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/) (Swagger UI)
- [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/) (ReDoc)
