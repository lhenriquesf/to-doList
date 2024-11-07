"""Módulo que define o modelo de usuário para o banco de dados.

Este módulo contém a definição do modelo `User`, que é usado para armazenar
informações de usuários no banco de dados. Ele inclui os campos de `id`, 
`username` e `password`, e uma configuração adicional para excluir a senha 
ao gerar representações Pydantic do modelo.
"""

from tortoise.models import Model
from tortoise.fields import IntField, CharField

class User(Model):
    """Modelo que representa um usuário no sistema.

    A classe `User` define os atributos básicos de um usuário, incluindo um
    identificador único `id`, um nome de usuário `username` e uma senha 
    criptografada `password`. O campo `password` é excluído ao gerar a 
    representação Pydantic para proteger a segurança dos dados.
    """
    id = IntField(pk=True)
    username = CharField(max_length=50, unique=True, null=False)
    password = CharField(max_length=128, null=False)

    class PydanticMeta:
        """Configurações adicionais para a geração de modelos Pydantic.

        A classe interna `PydanticMeta` é usada para personalizar o comportamento
        do modelo Pydantic gerado a partir do modelo `User`. Neste caso, ela
        configura para excluir o campo `password` ao gerar a representação do 
        modelo, visando proteger a privacidade da senha do usuário.
        """
        exclude = ["password"]
