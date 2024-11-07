"""Módulo que define os esquemas Pydantic para criação de usuários.

Este módulo contém os esquemas Pydantic usados para validar e serializar os
dados de criação de usuários, incluindo a verificação de correspondência de
senhas entre os campos `password` e `confirm_password`.
"""

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo

class UserCreate(BaseModel):
    """Esquema para criação de um novo usuário.

    Este esquema é usado para validar os dados ao criar um novo usuário. Ele
    garante que os campos `password` e `confirm_password` sejam válidos e que
    ambas as senhas correspondam.

    Attributes:
        username (str): Nome de usuário, com tamanho máximo de 50 caracteres.
        password (str): Senha, com comprimento mínimo de 4 caracteres.
        confirm_password (str): Confirmação da senha, com comprimento mínimo de 4 caracteres.
    """
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=4)
    confirm_password: str = Field(..., min_length=4)

    @field_validator('confirm_password')
    def passwords_match(cls, v, info: FieldValidationInfo):
        """
        Args:
            v (str): Valor do campo `confirm_password`.
            info (FieldValidationInfo): Informações sobre a validação do campo.

        Raises:
            ValueError: Se as senhas não forem iguais.

        Returns:
            str: O valor validado do campo `confirm_password`.
        """
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Senhas são diferentes')
        return v
