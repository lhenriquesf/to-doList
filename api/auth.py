from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from api.models.user_models import User
from pydantic import BaseModel
from jose import JWTError, jwt
from typing import Annotated
from typing import Optional
import os

# Carregando a chave secreta do ambiente
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Função para criar o token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para buscar o usuário no banco de dados
async def get_user_by_username(username: str):
    print("Função get_user_by_username", username)
    return await User.get_or_none(username=username)

# Função para autenticar o usuário
async def authenticate_user(username: str, password: str):
    print("Função authenticate_user")
    user = await get_user_by_username(username)
    print("Usuário", user)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

# Função para obter o usuário atual com base no token
async def get_current_user(token: Annotated[str, Depends(dependency=oauth2_scheme)]):
    print("Verificando usuário...")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais não validadas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    print("Decodificando token...")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload:", payload)
        username: str = payload.get("sub")
        print("Username:", username) 
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print("Erro ao decodificar o token:", e)
        raise credentials_exception

    user = await get_user_by_username(username)
    if user is None:
        print("Usuário não encontrado")
        raise credentials_exception
    return user
