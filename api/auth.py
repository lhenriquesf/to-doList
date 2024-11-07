"""Módulo de autenticação e criação de tokens JWT.

Este módulo contém funções para autenticação de usuários, geração e validação
de tokens JWT, e verificação do usuário atual com base no token de autenticação.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import JWTError, jwt

from api.models.user_models import User

# Carregando a chave secreta do ambiente
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    """Esquema do token de acesso."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Esquema para os dados do token de acesso."""
    username: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um token JWT com dados de expiração opcionais.

    Args:
        data (dict): Dados que serão codificados no token.
        expires_delta (Optional[timedelta]): Tempo de expiração do token.

    Returns:
        str: Token JWT codificado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_by_username(username: str) -> Optional[User]:
    """Busca um usuário no banco de dados pelo nome de usuário.

    Args:
        username (str): Nome de usuário a ser buscado.

    Returns:
        Optional[User]: Usuário encontrado ou None se não existir.
    """
    return await User.get_or_none(username=username)


async def authenticate_user(username: str, password: str) -> Optional[User]:
    """Autentica o usuário verificando o nome de usuário e a senha.

    Args:
        username (str): Nome de usuário do usuário.
        password (str): Senha em texto simples do usuário.

    Returns:
        Optional[User]: Usuário autenticado ou None se as credenciais forem inválidas.
    """
    user = await get_user_by_username(username)
    if user and pwd_context.verify(password, user.password):
        return user
    return None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Obtém o usuário atual com base no token JWT.

    Decodifica o token e verifica o nome de usuário associado. Levanta uma exceção
    caso o token seja inválido ou o usuário não seja encontrado.

    Args:
        token (str): Token JWT de autenticação.

    Returns:
        User: Usuário autenticado.

    Raises:
        HTTPException: Caso o token seja inválido ou o usuário não seja encontrado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais não validadas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = await get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user
