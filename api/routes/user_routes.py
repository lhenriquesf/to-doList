"""Módulo das rotas de usuário.

Este módulo define as rotas de autenticação e registro de usuários. 
Inclui a criação de novos usuários, com hash de senha para segurança, e 
a geração de tokens de autenticação para acesso seguro a rotas protegidas.
"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from api.auth import create_access_token, authenticate_user, Token
from api.schemas.user_schemas import UserCreate
from api.models.user_models import User

user_router = APIRouter(prefix="/auth", tags=["User"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    """Gera um hash para a senha fornecida.

    Args:
        password (str): A senha em texto simples.

    Returns:
        str: A senha criptografada.
    """
    return pwd_context.hash(password)


@user_router.post("/register", status_code=201)
async def register(user_data: UserCreate):
    """
    Rota para registrar um novo usuário.

    Verifica se o usuário já existe; caso contrário, cria um novo usuário
    com uma senha criptografada e armazena no banco de dados.

    Args:
        user_data (UserCreate): Dados do usuário para registro.

    Returns:
        dict: Mensagem de confirmação do registro.
    """
    user_exists = await User.filter(username=user_data.username).exists()
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="Usuário já existe",
        )

    hashed_password = get_password_hash(user_data.password)
    await User.create(username=user_data.username, password=hashed_password)

    return {"message": "Usuário registrado com sucesso"}


@user_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    Rota para autenticação de um usuário.

    Verifica as credenciais do usuário e, se válidas, gera um token de acesso.

    Args:
        form_data (OAuth2PasswordRequestForm): Dados de login do usuário.

    Returns:
        Token: Token de acesso gerado para o usuário autenticado.
    
    Raises:
        HTTPException: Se as credenciais forem inválidas.
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
