FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
# Inicia o servidor Gunicorn na porta 5000
# app:app = primeiro 'app' é o arquivo app.py, segundo é a variável app = Flask(__name__)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]