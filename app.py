
from flask import Flask,jsonify,request
import os
import psycopg2

app = Flask(__name__)

# Funções que vão ser usadas para conectar ao banco de dados
def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"]) # Obtendo a URL do banco de dados a partir da 
                                                        # variável de ambiente DATABASE_URL que definimos no docker-compose.yml
def criar_tabela():
    conn = get_connection() # Obtendo a conexão com o banco de dados
    cursor = conn.cursor() # Criando um cursor para executar comandos SQL
    cursor.execute("""       
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            concluida BOOLEAN DEFAULT FALSE
        );
    """)  # Criando a tabela "tarefas" caso ela não exista
    conn.commit() # confirma a operação no banco, sem isso a mudança não é salva
    cursor.close() # fecha o cursor, liberando recursos
    conn.close() # fecha a conexão com o banco, liberando recursos

#Rotas que o flask vai ficar escutando

####  Define qual método HTTP a rota aceita. GET = buscar dados, POST = criar, PUT = atualizar, DELETE = remover ####
@app.route("/api/tarefas", methods=["GET"])
def listar_tarefas():
    conn = get_connection() # Obtendo a conexão com o banco de dados
    cursor = conn.cursor() # Criando um cursor para executar comandos SQL
    cursor.execute("SELECT id, titulo, concluida FROM tarefas;") # Executando um comando SQL para selecionar todas as tarefas
    tarefas = [{"id": row[0], "titulo": row[1], "concluida": row[2]} for row in cursor.fetchall()]  ## Transforma cada linha do banco em um dicionário python e retorna as linhas do resultado da query
    cursor.close() # fecha o cursor, liberando recursos
    conn.close() # fecha a conexão com o banco, liberando recursos
    return jsonify(tarefas) # Retorna a lista de tarefas em formato JSON

@app.route("/api/tarefas", methods=["POST"])
def criar_tarefa():
    dados = request.get_json() # Obtendo os dados da requisição em formato JSON
    conn = get_connection() # Obtendo a conexão com o banco de dados
    cursor = conn.cursor() # Criando um cursor para executar comandos SQL
    cursor.execute("INSERT INTO tarefas (titulo) VALUES (%s) RETURNING id", (dados["titulo"],)) # Executando um comando SQL para inserir uma nova tarefa, usando o título fornecido na requisição"))
    id_novo = cursor.fetchone()[0] # Obtendo o ID da nova tarefa inserida
    conn.commit() # confirma a operação no banco, sem isso a mudança não é salva
    cursor.close() # fecha o cursor, liberando recursos
    conn.close() # fecha a conexão com o banco, liberando recursos
    return jsonify({"id": id_novo, "titulo": dados["titulo"], "concluida": False}), 201 # Retorna os dados da nova tarefa em formato JSON, com status code 201 (Criado)

@app.route("/api/tarefas/<int:id>", methods=["PUT"])
def concluir_tarefa(id):
    conn = get_connection() # Obtendo a conexão com o banco de dados
    cursor = conn.cursor() # Criando um cursor para executar comandos SQL
    cursor.execute("UPDATE tarefas SET concluida = TRUE WHERE id = %s", (id,)) # Executando um comando SQL para atualizar a tarefa com o ID fornecido, usando os dados fornecidos na requisição
    conn.commit() # confirma a operação no banco, sem isso a mudança não é salva
    cursor.close() # fecha o cursor, liberando recursos
    conn.close() # fecha a conexão com o banco, liberando recursos
    return jsonify({"mensagem": "Tarefa concluída com sucesso!"}) # Retorna os dados da tarefa atualizada em formato JSON

@app.route ("/api/tarefas/<int:id>", methods = ["DELETE"])
def deletar_tarefa(id):
    conn = get_connection() # Obtendo a conexão com o banco de dados
    cursor = conn.cursor() # Criando um cursor para executar comandos SQL
    cursor.execute("DELETE FROM tarefas WHERE id = %s", (id,))
    conn.commit() # confirma a operação no banco, sem isso a mudança não é salva
    cursor.close() # fecha o cursor, liberando recursos
    conn.close() # fecha a conexão com o banco, liberando recursos
    return jsonify({"mensagem": "Tarefa deletada com sucesso!"}) # Retorna os dados da tarefa atualizada em formato JSON

if __name__ == "__main__":
    criar_tabela() # Chama a função para criar a tabela "tarefas" no banco de dados
    app.run(host="0.0.0.0", port = 5000)