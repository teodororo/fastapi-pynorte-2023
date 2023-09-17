# fastapi-pynorte-2023
Código e slides do workshop apresentado na Python Norte 2023.

## Instalação
Python 3.6+

```pip3 install "fastapi[all]"```

```pip3 install pytest-cov```

## Agenda
- [Hello, world!](#hello-world)
- [Troubleshooting](#troubleshooting)

```Python
```


## Hello, world!
```Python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
	return {"hello":"world"}
```
Para executar, assumindo que o arquivo se chama "main.py":
```console
uvicorn main:app --reload```
Caso queira rodar em segundo plano, adicione "&" no final do comando. Há outras opções de parâmetros, por exemplo:
```console
uvicorn main:app --reload --host 0.0.0.0 --port 88 --workers 4 ... &```
Saiba mais na [documentação oficial do Uvicorn](https://www.uvicorn.org/).
Se rodarmos:

```console
pytest --cov=. --cov-report=html```

E abrimos o diretório "htmlcov", o arquivo "main_py.html" irá nos informar que nada foi testado.
Então, crie um arquivo chamado "test_hello_world.py" e copie o seguinte _script_:
```Python
from fastapi.testclient import TestClient
from main import app

def test_hello_world():
	client = TestClient(app)
	response = client.get('/')
	assert response.status_code == 200
	assert response.json() == {'hello': 'world'}
```
Agora, ao rodar o comando:

```console
pytest --cov=. --cov-report=html```

O "main_py.html" estará todo verde.


## Troubleshooting
Para parar o FastAPI:

```console
fuser -k 8000/tcp```
