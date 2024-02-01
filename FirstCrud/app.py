import pyodbc
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Configurações de conexão ao SQL Server com autenticação do Windows
server = 'G15-5530\SQLEXPRESS'
database = 'Form'
driver = 'ODBC Driver 17 for SQL Server'
trusted_connection = 'yes'  # Usar autenticação do Windows

# String de conexão para autenticação do Windows
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'

@app.route("/")
@app.route("/index")
def index():
    # Conectar ao SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Executar a consulta para selecionar todos os registros da tabela users
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    # Fechar a conexão
    conn.close()

    return render_template("index.html", datas=data)

@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        rua = request.form["rua"]
        cidade = request.form["cidade"]
        numero = request.form["numero"]
        estado = request.form["estado"]
        email = request.form["email"]

        # Conectar ao SQL Server
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Executar a inserção no banco de dados
        cursor.execute("INSERT INTO users(NOME, IDADE, RUA, CIDADE, NUMERO, ESTADO, EMAIL) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (nome, idade, rua, cidade, numero, estado, email))
        conn.commit()
        conn.close()

        flash("Dados cadastrados", "success")
        return redirect(url_for("index"))

    return render_template("add_user.html")

@app.route("/edit_user/<int:id>", methods=["POST", "GET"])
def edit_user(id):
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        rua = request.form["rua"]
        cidade = request.form["cidade"]
        numero = request.form["numero"]
        estado = request.form["estado"]
        email = request.form["email"]

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Executar a atualização no banco de dados
        cursor.execute("UPDATE users SET NOME=?, IDADE=?, RUA=?, CIDADE=?, NUMERO=?, ESTADO=?, EMAIL=? WHERE ID=?", (nome, idade, rua, cidade, numero, estado, email, id))
        conn.commit()

        conn.close()

        flash("Dados cadastrados", "success")
        return redirect(url_for("index"))

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE ID=?", (id,))
    data = cursor.fetchone()

    conn.close()

    return render_template("edit_user.html", datas=data)

@app.route("/delete_user/<int:id>", methods=["GET"])
def delete_user(id):
    # Conectar ao SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Executar a exclusão no banco de dados
    cursor.execute("DELETE FROM users WHERE ID=?", (id,))
    conn.commit()
    conn.close()

    flash("Dados deletados", "warning")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.secret_key = "admin123"
    app.run(debug=True)
