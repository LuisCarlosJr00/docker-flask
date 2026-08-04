#--- Instalação das Dependencias ---#

FROM python:3.8-slim AS builder
WORKDIR /app
COPY requirements.txt .

# --- Instala as dependencias numa pasta isolada (não no sistema)
RUN pip install--prefix=/install -r requirements.txt

# --- Cria a imagem final ---#
FROM python:3.8-slim
WORKDIR /app

# --- Copia Apenas as dependencias instaladas para a imagem final ---#
COPY --from=builder /install /usr/local 

# --- Copia o código da aplicação para a imagem final ---#
COPY . .

# Inicia o servidor Gunicorn na porta 5000
# app:app = primeiro 'app' é o arquivo app.py, segundo é a variável app = Flask(__name__)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]