"""
Módulo de configuração da aplicação FastAPI.

Este módulo contém a configuração da aplicação FastAPI, incluindo a 
configuração do middleware CORS, o registro das rotas da API, e a 
configuração do banco de dados utilizando o Tortoise ORM. Também carrega 
as variáveis de ambiente a partir de um arquivo .env.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv

from api.routes.task_routes import task_router
from api.routes.user_routes import user_router

# Carregando variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()

# Definindo as origens permitidas para CORS
origins = [
    "https://frontend-todo-list-chi.vercel.app",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

# Configurando middleware para permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Registrando as rotas da API
app.include_router(task_router)
app.include_router(user_router)

# Configuração do banco de dados com Tortoise ORM
register_tortoise(
    app=app,
    db_url="sqlite://task.db",  # URL do banco de dados
    add_exception_handlers=True,  # Adicionar manipuladores de exceção
    generate_schemas=True,  # Gerar esquemas automaticamente
    modules={
        "models": [
            "api.models.task_models", 
            "api.models.user_models"
        ]
    },  # Modelos a serem registrados
)


@app.get("/")
async def ler_root():
    """
    Rota raiz da aplicação.

    Retorna uma mensagem simples de boas-vindas.

    Returns:
        dict: Mensagem de status indicando que a API está funcionando.
    """
    return {"message": "Hello World"}
