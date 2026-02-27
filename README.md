Backend de Registro de Pedidos de Doces

Descrição

Este projeto é o backend de um sistema para registro e gerenciamento de pedidos de doces. Ele foi desenvolvido utilizando Python com o framework Flask e MongoDB como banco de dados. O sistema permite registrar novos pedidos, buscar, atualizar, deletar, listar, filtrar e paginar pedidos, além de funcionalidades para atualização e exclusão em massa. É importante notar que este backend não inclui funcionalidades de delivery, focando exclusivamente no gerenciamento interno dos pedidos.

Funcionalidades

•
Registro de Pedidos: Criação de novos pedidos com detalhes como nome do cliente, itens, quantidades, preços e status.

•
Busca de Pedidos: Recuperação de pedidos específicos por ID.

•
Atualização de Pedidos: Modificação de informações de pedidos existentes, incluindo o status.

•
Listagem de Pedidos: Visualização de todos os pedidos registrados.

•
Paginação: Listagem de pedidos com suporte a paginação para grandes volumes de dados.

•
Contagem de Pedidos: Contagem de pedidos com base em critérios de filtro.

•
Filtro de Pedidos: Filtragem de pedidos por diversos critérios.

•
Atualização em Massa: Atualização de múltiplos pedidos simultaneamente.

•
Incremento de Itens: Incremento de quantidades de itens em pedidos.

•
Exclusão de Pedidos: Remoção de pedidos individuais.

•
Exclusão em Massa: Remoção de múltiplos pedidos simultaneamente.

Tecnologias Utilizadas

•
Python: Linguagem de programação principal.

•
Flask: Microframework web para Python.

•
PyMongo: Driver Python para MongoDB.

•
MongoDB: Banco de dados NoSQL para armazenamento dos pedidos.

•
Cerberus: Biblioteca para validação de esquemas de dados.

Dependências

As seguintes bibliotecas Python são utilizadas neste projeto:

Plain Text


blinker==1.9.0
Cerberus==1.3.8
click==8.3.1
colorama==0.4.6
dnspython==2.8.0
Flask==3.1.3
iniconfig==2.3.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
packaging==26.0
pluggy==1.6.0
Pygments==2.19.2
pymongo==4.16.0
pytest==9.0.2
Werkzeug==3.1.6



Estrutura do Projeto

Plain Text


modulo_11_MongoDB/
├── run.py
├── requirements.txt
└── src/
    ├── __init__.py
    ├── errors/
    │   ├── __init__.py
    │   ├── error_handler.py
    │   └── types/
    ├── main/
    │   ├── __init__.py
    │   ├── composer/
    │   ├── http_types/
    │   ├── routes/
    │   │   └── delivery_routes.py
    │   └── server/
    │       └── server.py
    │   └── validators/
    │       └── registry_order_validator.py
    ├── models/
    │   ├── __init__.py
    │   ├── connection/
    │   │   └── connection_handler.py
    │   └── repository/
    │       └── orders_repository.py
    └── use_cases/
        ├── __init__.py
        ├── count_orders.py
        ├── delete_many_orders.py
        ├── delete_order.py
        ├── filter_orders.py
        ├── increment_orders.py
        ├── list_of_orders.py
        ├── registry_finder.py
        ├── registry_order.py
        ├── registry_updater.py
        ├── search_with_pagination.py
        ├── update_many_orders.py
        └── update_order_status.py



Como Rodar o Projeto

Pré-requisitos

•
Python 3.x

•
MongoDB instalado e rodando (na porta padrão 27017, ou configurar a string de conexão em src/models/connection/connection_handler.py )

Instalação

1.
Clone o repositório (se aplicável, ou descompacte o arquivo):

Bash


git clone <URL_DO_REPOSITORIO>
cd modulo_11_MongoDB



ou

Bash


unzip modulo_11_MongoDB.zip
cd modulo_11_MongoDB





2.
Crie e ative um ambiente virtual:

Bash


python3 -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate    # Windows





3.
Instale as dependências:

Bash


pip install -r requirements.txt





Execução

Para iniciar o servidor Flask:

Bash


python run.py



O servidor estará disponível em http://0.0.0.0:3000.

Endpoints da API

Todos os endpoints estão sob o prefixo /delivery. Embora o nome do blueprint seja delivery_routes, o sistema não possui funcionalidades de entrega, sendo o nome apenas uma convenção interna.

