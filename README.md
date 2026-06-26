# To-Do App com Docker

Aplicação web de lista de tarefas desenvolvida como projeto de aprendizado de Docker, containerização e arquitetura de aplicações web.

## Tecnologias

- **Python + Flask** — API REST do backend
- **PostgreSQL** — banco de dados relacional
- **NGINX** — servidor web e reverse proxy
- **Docker + Docker Compose** — containerização e orquestração dos serviços

## Arquitetura

```
Usuário
  ↓
NGINX (porta 8888)
  ├── Serve o frontend (HTML/CSS/JS)
  └── Redireciona /api/ → Flask (porta 5000)
                            ↓
                       PostgreSQL (porta 5432)
```

## Funcionalidades

- Criar tarefas
- Listar tarefas
- Concluir tarefas
- Excluir tarefas

## Como rodar localmente

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado

### Configuração

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/docker-flask.git
cd docker-flask
```

2. Crie o arquivo `.env` na raiz do projeto:
```
POSTGRES_USER=usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=tarefas
DATABASE_URL=postgresql://usuario:sua_senha@db:5432/tarefas
```

3. Suba os containers:
```bash
docker compose up -d
```

4. Acesse no navegador: [http://localhost:8888](http://localhost:8888)

### Parar a aplicação

```bash
docker compose down
```

## Estrutura do projeto

```
docker-flask/
├── app.py                  # API Flask com rotas CRUD
├── requirements.txt        # Dependências Python
├── Dockerfile              # Imagem do backend
├── docker-compose.yml      # Orquestração dos containers
├── .env                    # Variáveis de ambiente (não versionado)
├── .gitignore
├── nginx/
│   └── nginx.conf          # Configuração do servidor web
└── frontend/
    └── index.html          # Interface da aplicação
```
