# 📦 API de Gestão Comercial
Esta aplicação é uma API RESTful desenvolvida com FastAPI para gestão de clientes, produtos e pedidos de uma empresa do setor comercial. O sistema foi projetado para servir como back-end de uma interface que possibilita o controle de vendas, catálogo de produtos e atendimento ao cliente.

# ✨ Funcionalidades

- Autenticação e autorização com JWT, incluindo refresh token.
- CRUD completo para clientes, produtos e pedidos.
- Filtros avançados e paginação nos endpoints.
- Validação de dados (como CPF e e-mail únicos).
- Níveis de acesso (usuário comum e admin).
- Migrations de banco de dados com Alembic.
- Suporte para envio de mensagens via WhatsApp API (em desenvolvimento).

# 🛠️ Tecnologias utilizadas
* Python 3.11+
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* PyJWT
* Pytest
* Docker
* Pydantic
* Uvicorn

# 📚 Organização
O projeto segue uma estrutura modular com separação por responsabilidade:

router/ – Definição das rotas da API.
service/ – Regras de negócio e lógica de aplicação.
database/ – Modelos e configurações de banco de dados.
tests/ – Testes automatizados com pytest.

# 🚀 Como executar
Em breve será incluído um arquivo docker-compose.yml para facilitar a execução local. Por enquanto, você pode rodar localmente com os comandos abaixo:

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Execute as migrations
alembic upgrade head

# Inicie a aplicação
uvicorn main:app --reload
