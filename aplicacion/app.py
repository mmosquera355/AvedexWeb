#---------------------------------------------------------------------
# Programa principal de avedex, renderización de templates, crud de base de datos y logica.
# Avedex main program, template rendering, database and logic.
# Maria Angelica Mosquera Moreno
# gihub: mmosquera355
# Julio 2020
# ---------------------------------------------------------------------

#Importaciones de librerias
# Library imports
import os
import zipfile
from flask import Flask, render_template, request
from flask import send_file
from flask import flash
from flask_material import Material
import psycopg2
from flask_toastr import Toastr

app = Flask(__name__)
Material(app)
toastr = Toastr(app)
toastr.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#conexion con la bd
connection = psycopg2.connect(user="postgres",
                                password="1234",
                                host="127.0.0.1",
                                port="5432",
                                database="pAvedex")
#DB_URI = "postgresql+psycopg2://{username}:{password}@{hostname}/{databasename}".format(username="postgres", password="1234", hostname="localhost", databasename="avedex")
#app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

'''Definifición de rutas'''
@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404

@app.route('/layoutlogin')
def layoutlogin():
    return render_template("login.html")


@app.route('/layoutRegistro')
def layoutRegistro():
    return render_template("registro.html")


'''Consultas a la base de datos'''
def getAllData(sentencia):
    try:
        cursor = connection.cursor()
        postgreSQL_select_Query = sentencia
        cursor.execute(postgreSQL_select_Query)
        datos = cursor.fetchall()  
        cursor.close()
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    return datos

def insertData(sentenciaInsert, info, accion):
    try:
        cursor = connection.cursor()
        cursor.execute(sentenciaInsert, info)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into table")
        if(accion == "eliminar"):
            flash("Registro eliminado correctamente")
        if(accion == "insertar"):
            flash("Registro insertado correctamente")
        if(accion == "actualizar"):
            flash("Registro actualizado correctamente")


    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into table", error)

@app.route("/")
def upload_file():
    return render_template("panelMenu.html")

@app.route('/registro',  methods=['POST'])
def registro():
    email = request.form.get("user")
    print(email)
    password = request.form.get("pass")
    print(password)
    print( "'{0}'".format(password))
    try:
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO login (codigo, email, password, codigo_especialidad) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (1, email, password,1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into login table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into table", error)

    return render_template("registro.html")


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get("user")
    print(email)
    password = request.form.get("pass")
    print(password)
    print( "'{0}'".format(password))
    try:
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO login (codigo, email, password, codigo_especialidad) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (1, email, password,1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into login table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into table", error)

    return render_template("login.html")


'''Tabla de usuarios'''

@app.route('/usuarios', methods=['GET','POST'])
def usuarios():

    usuarios = getAllData('select * from usuario ORDER BY codigo')
    especialidades =  getAllData('select * from especialidad')

    if request.method == 'POST':
        id = request.form.get("idusr")
        print(id)
        username = request.form.get("username")
        print(username)
        email = request.form.get("email")
        print(email)
        password = request.form.get("pass")
        print(password)
        especialidad = request.form.get('especialidad')
        codigo = request.form.get("idusrEl")
        print(codigo)
        valor = request.form.get("valor")
        valorUno = request.form.get("valorUno")
        print(valor)
        if(valor is None):
            if(id!=''):
                print("actualizaremos")
                sql_update_query = """Update usuario set nombre = %s, email = %s, codigo_especialidad= %s where codigo = %s"""
                record_to_update = (username, email, especialidad,id)
                insertData(sql_update_query,record_to_update, valorUno)

            else:
                print("insertaremos")
                postgres_insert_query = """ INSERT INTO usuario (nombre, email, codigo_especialidad) VALUES (%s,%s,%s)"""
                record_to_insert = (username, email, especialidad)
                insertData(postgres_insert_query,record_to_insert, valorUno)
                postgres_insert_query = """ INSERT INTO login (email, password, codigo_especialidad) VALUES (%s,%s,%s)"""
                record_to_insert = (email, password, especialidad) 
                insertData(postgres_insert_query,record_to_insert, valorUno)
        else:
            print(valor)
            sql_delete_query = """Delete from usuario where codigo = %s"""
            record_to_delete = (codigo,)
            insertData(sql_delete_query,record_to_delete, valor)  
        
        #realizando de nuevo las consultas
        usuarios = getAllData('select * from usuario ORDER BY codigo')
        especialidades =  getAllData('select * from especialidad')
    return render_template("usuarios.html", usuarios = usuarios, especialidades = especialidades )

@app.route('/eliminarUsuario', methods=['GET','POST'])
def eliminarUsuario():
    if request.method == 'POST':
        print("entrando a eliminar usuario")
        codigo = request.form.get("idusrEl")
        print(codigo)
        valor = request.form.get("valor")
        print(valor)
        #sql_delete_query = """Delete from usuario where codigo = %s"""
        #record_to_delete = (id)
        #insertData(sql_delete_query,record_to_delete)
        usuarios = getAllData('select * from usuario ORDER BY codigo')
        especialidades =  getAllData('select * from especialidad')
    return render_template("usuarios.html", usuarios = usuarios, especialidades = especialidades )


