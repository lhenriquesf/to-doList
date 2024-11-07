"""
Este módulo é responsável por iniciar o servidor Uvicorn para a aplicação FastAPI.

Ele verifica se o arquivo está sendo executado diretamente e, em caso afirmativo,
inicia o servidor na porta 8000 com a opção de recarga automática ativada para
ambientes de desenvolvimento.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
