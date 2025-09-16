# Pokemon Trainer API

### Uma API interativa para treinadores Pokémon, desenvolvida em Python com FastAPI, que se integra com a PokeAPI e um banco de dados para gerenciar informações de treinadores e suas capturas.
### 🚀 Tecnologias Utilizadas

    FastAPI (v0.116.1) - Framework web moderno e rápido para APIs

    Pydantic (v2.10.2) - Validação de dados e configuração usando tipos Python

    SQLAlchemy (v2.0.23) - ORM para interação com banco de dados

    Uvicorn (v0.24.0) - Servidor ASGI para execução da aplicação

    HTTPX (v0.28.1) - Cliente HTTP assíncrono para integrações com APIs externas

## 📋 Funcionalidades

    Gerenciamento de treinadores Pokémon (criação, consulta, atualização e exclusão)

    Captura de Pokémon em localizações aleatórias

    Consulta de informações da PokeAPI

    Atualização de localização do jogador

    Listagem de todos os treinadores cadastrados

## 🏗️ Estrutura do Projeto

    ├── main.py             # Arquivo principal da aplicação FastAPI
    ├── schemes.py          # Esquemas Pydantic para validação de dados
    ├── Dockerfile          # Configuração do container Docker
    ├── docker-compose.yml  # Orquestração de containers
    └── requirements.txt    # Dependências do projeto

## 🔧 Configuração e Instalação
Pré-requisitos

    Docker

    Docker Compose

Executando a Aplicação

    Clone o repositório:

bash

git clone <url-do-repositorio>
cd <diretorio-do-projeto>

    Execute o Docker Compose:

bash

docker-compose up

    A API estará disponível em: http://localhost:8000

    Acesse a documentação interativa da API:

        Swagger UI: http://localhost:8000/docs

        ReDoc: http://localhost:8000/redoc

## 📡 Endpoints Principais
Treinadores

    GET /getTrainer/{trainer_name} - Obtém informações de um treinador

    POST /createTrainer - Cria um novo treinador

    PATCH /updatePlayerLocation/ - Atualiza a localização de um treinador

    DELETE /deleteTrainer/{trainer_name} - Remove um treinador

    GET /listAllTrainers/ - Lista todos os treinadores

Pokémon

    POST /capturePokemon/ - Captura um Pokémon em uma localização

    GET /getAreaRandomPokemon/{location_name} - Obtém um Pokémon aleatório de uma área

    GET /listPokemons/ - Lista todos os pokemons de um treinador

Localizações

    GET /randomLocation/ - Obtém uma localização aleatória

    GET /randomArea/{location_name} - Obtém uma área aleatória de uma localização

    GET /location/{location_name} - Obtém informações de uma localização específica

## 🔌 Integrações
PokeAPI

A aplicação se integra com a PokeAPI para obter informações sobre:

    Pokémon

    Localizações

    Áreas de encontro

API de Banco de Dados

A aplicação se comunica com uma API de banco de dados separada para:

    Armazenar informações dos treinadores

    Registrar Pokémon capturados

    Gerenciar localizações dos jogadores

## 🐳 Configuração Docker

O projeto utiliza Docker Compose para orquestrar dois serviços:

    main_api: A API principal (esta aplicação)

    db_api: API de banco de dados para persistência

A rede é configurada com bridge mode para facilitar a comunicação entre os containers.

##📝 Esquemas de Dados

Os principais esquemas utilizados na API incluem:

    TrainerSchema: Representa um treinador Pokémon

    PokemonSchema: Representa um Pokémon

    Location: Representa uma localização do mundo Pokémon

    CapturePokemonSchema: Esquema para requisição de captura de Pokémon


## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.
## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
