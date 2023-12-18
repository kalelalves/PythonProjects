from   flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app=Flask(__name__)

@app.route("/")
@app.route("/index")


def index():
    con = sql.connect("from_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users")
    data=cur.fetchall()
    return render_template("index.html",datas=data)

@app.route("/add_user",methods=["POST","GET"])
def add_user():
    if request.method=="POST":
        nome=request.form["nome"]
        idade=request.form["idade"]
        rua=request.form["rua"]
        cidade=request.form["cidade"]
        numero=request.form["numero"]
        estado=request.form["estado"]
        email=request.form["email"]
        con= sql.connect("from_db.db")
        cur= con.cursor()
        cur.execute("insert into users(NOME, IDADE, RUA, CIDADE, NUMERO, ESTADO, EMAIL) values (?,?,?,?,?,?)",(nome, idade, rua, cidade, numero, estado, email))
        con.commit()
        flash("Dados cadastrados,", "success")
        return redirect(url_for("index"))    
    return render_template("add_user.html")  

