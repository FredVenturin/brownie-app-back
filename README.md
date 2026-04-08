# Brownies Delivery API

REST API para gerenciamento de pedidos, clientes e produtos de um negócio de venda de doces. Permite criar, editar, listar e remover registros, além de calcular métricas de lucro com base nos pedidos realizados.

## Tecnologias

- Python 3.11
- Flask
- MongoDB / PyMongo
- Flask-CORS
- Cerberus
- Gunicorn

## Funcionalidades

- CRUD completo de pedidos, clientes e produtos
- Soft-delete com lixeira e restauração
- Listagem paginada com filtros de busca
- Atualização de status de pedidos
- Ações em massa sobre pedidos
- Estatísticas de pedidos por status em consulta única
- Resumo de lucro diário, mensal, anual e total em consulta única
- Lucro por período específico (ano, mês, dia)

## Arquitetura

O projeto segue arquitetura em camadas com separação de responsabilidades:

```
src/
├── main/
│   ├── server/       # configuração do Flask
│   ├── routes/       # definição dos endpoints
│   ├── composer/     # injeção de dependências
│   └── validators/   # validação de entrada
├── models/
│   ├── connection/   # conexão e índices do MongoDB
│   └── repository/   # acesso ao banco de dados
└── use_cases/        # regras de negócio
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=nome_do_banco
CORS_ORIGINS=http://localhost:5173
```

Para produção com MongoDB Atlas, substitua `MONGO_URI` pela string de conexão do cluster.

## Executando localmente

```bash
# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar
python run.py
```

API disponível em `http://localhost:3000`.

## Endpoints

### Pedidos

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/delivery/order` | Criar pedido |
| `GET` | `/delivery/order/{id}` | Buscar por ID |
| `PATCH` | `/delivery/order/{id}` | Editar pedido |
| `PATCH` | `/delivery/order/{id}/status` | Atualizar status |
| `DELETE` | `/delivery/order/{id}` | Excluir pedido |
| `GET` | `/delivery/orders` | Listagem paginada |
| `GET` | `/delivery/orders/filter` | Filtrar pedidos |
| `GET` | `/delivery/orders/count` | Contar pedidos |
| `GET` | `/delivery/orders/stats` | Estatísticas por status |

### Clientes

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/delivery/clients` | Listar clientes |
| `POST` | `/delivery/clients` | Criar cliente |
| `PATCH` | `/delivery/clients/{id}` | Editar cliente |
| `DELETE` | `/delivery/clients/{id}` | Excluir cliente |

### Produtos

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/delivery/products` | Listar produtos |
| `POST` | `/delivery/products` | Criar produto |
| `PATCH` | `/delivery/products/{id}` | Editar produto |
| `DELETE` | `/delivery/products/{id}` | Excluir produto |

### Lucro

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/delivery/profit/summary` | Resumo diário, mensal, anual e total |
| `GET` | `/delivery/profit?year=2026` | Lucro anual |
| `GET` | `/delivery/profit?year=2026&month=3` | Lucro mensal |
| `GET` | `/delivery/profit?year=2026&month=3&day=5` | Lucro diário |

O lucro é calculado considerando apenas pedidos com status `sold`.

## Deploy

```bash
gunicorn -b 0.0.0.0:$PORT app:app
```

Configure as variáveis de ambiente no painel do provedor (Railway, Render, etc.). O domínio do frontend deve estar autorizado em `CORS_ORIGINS`.
