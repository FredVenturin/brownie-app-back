README.md — Backend
Brownies Delivery API (Backend)

API REST para registro e gerenciamento de pedidos, clientes e produtos de um negócio de venda de doces.

A aplicação permite criar, editar, listar e remover pedidos, além de gerenciar clientes e produtos utilizados nas vendas. Também possui endpoints para métricas de lucro baseadas nos pedidos vendidos.

A API foi construída utilizando Python, Flask e MongoDB, seguindo uma arquitetura em camadas com separação entre rotas, casos de uso e repositórios.

Tecnologias utilizadas

Python 3.11<br>
Flask<br>
MongoDB<br>
PyMongo<br>

Flask-CORS

Cerberus

Gunicorn

Funcionalidades
Pedidos

Criar pedido

Buscar pedido por ID

Atualizar pedido

Atualizar status do pedido

Deletar pedido

Listar pedidos

Listagem paginada

Filtros de busca

Contagem de pedidos

Ações em massa

Clientes

Criar cliente

Listar clientes

Editar cliente

Deletar cliente

Produtos

Criar produto

Listar produtos

Editar produto

Deletar produto

Lucro

Resumo de lucro diário

Resumo de lucro mensal

Resumo de lucro anual

Lucro total

Consulta de lucro por período específico

Estrutura do projeto
.
├── run.py
├── requirements.txt
└── src
    ├── main
    │   ├── server
    │   ├── routes
    │   ├── composer
    │   └── validators
    ├── models
    │   ├── connection
    │   └── repository
    └── use_cases

A estrutura segue o padrão de separação de responsabilidades:

routes definem os endpoints

composer monta dependências

use_cases contém regras de negócio

repository comunica com o banco de dados

Variáveis de ambiente

Crie um arquivo .env na raiz do projeto.

MONGO_URI=mongodb://localhost:27017
DB_NAME=brownies
CORS_ORIGINS=http://localhost:5173

Caso utilize MongoDB Atlas, use a string de conexão fornecida pelo cluster.

Executando o projeto localmente
1 ) Criar ambiente virtual
python -m venv venv
2) Ativar ambiente virtual

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate
3) Instalar dependências
pip install -r requirements.txt
4) Rodar a aplicação
python run.py

A API iniciará normalmente em:

http://localhost:3000

Endpoints principais
Pedidos

Criar pedido
POST /delivery/order

Buscar pedido por ID
GET /delivery/order/{order_id}

Atualizar pedido
PATCH /delivery/order/{order_id}

Atualizar status do pedido
PATCH /delivery/order/{order_id}/status

Deletar pedido
DELETE /delivery/order/{order_id}

Listagem paginada
GET /delivery/orders?page=1&limit=10

Filtrar pedidos
GET /delivery/orders/filter

Contar pedidos
GET /delivery/orders/count

Clientes

Listar clientes
GET /delivery/clients

Criar cliente
POST /delivery/clients

Editar cliente
PATCH /delivery/clients/{client_id}

Deletar cliente
DELETE /delivery/clients/{client_id}

Produtos

Listar produtos
GET /delivery/products

Criar produto
POST /delivery/products

Editar produto
PATCH /delivery/products/{product_id}

Deletar produto
DELETE /delivery/products/{product_id}

Lucro

Resumo geral
GET /delivery/profit/summary

Lucro por período
GET /delivery/profit?year=2026
GET /delivery/profit?year=2026&month=3
GET /delivery/profit?year=2026&month=3&day=5

O lucro é calculado considerando pedidos com status sold.

Deploy

Exemplo de comando recomendado para produção:

gunicorn -b 0.0.0.0:3000 run:app

Configure as variáveis de ambiente no provedor (Render, Railway etc. ).

Integração com frontend

O frontend consome endpoints sob o prefixo:

/delivery

Garanta que o domínio do frontend esteja autorizado em:

CORS_ORIGINS

Licença

Projeto desenvolvido para fins educacionais e uso prático em um negócio de doces.
