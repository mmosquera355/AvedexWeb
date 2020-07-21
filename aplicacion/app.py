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
    return render_template("error.html", error="Página no encontrada... te invitamos a ingresar una dirección valida."), 404

@app.route("/")
def upload_file():
    return render_template("panelMenu.html")

@app.route('/layoutPanel')
def layoutPanel():
    return render_template("panelMenu.html")

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


'''Tabla de usuarios y login'''

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
                sql_update_query = """Update login set email = %s, codigo_especialidad= %s where email = %s"""
                record_to_update = (email, especialidad,email)
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

''' tabla de misiones '''

@app.route('/misiones', methods=['GET','POST'])
def misiones():

    misiones = getAllData('select * from mision ORDER BY codigo')

    if request.method == 'POST':
        id = request.form.get("idmis")
        print(id)
        titulo = request.form.get("nombre")
        print(titulo)
        descripcion = request.form.get("descripcion")
        print(descripcion)
        puntos = request.form.get("puntos")
        print(puntos)
        codigo = request.form.get("idmisEl")
        print(codigo)
        valor = request.form.get("valor")
        valorUno = request.form.get("valorUno")
        print(valor)
        if(valor is None):
            if(id!=''):
                print("actualizaremos")
                sql_update_query = """Update mision set nombre = %s, descripcion = %s, puntos= %s where codigo = %s"""
                record_to_update = (titulo, descripcion, puntos,id)
                insertData(sql_update_query,record_to_update, valorUno)

            else:
                print("insertaremos")
                postgres_insert_query = """ INSERT INTO mision (nombre, descripcion, puntos) VALUES (%s,%s,%s)"""
                record_to_insert = (titulo, descripcion, puntos)
                insertData(postgres_insert_query,record_to_insert, valorUno)
        else:
            print(valor)
            sql_delete_query = """Delete from mision where codigo = %s"""
            record_to_delete = (codigo,)
            insertData(sql_delete_query,record_to_delete, valor) 
        
        #realizando de nuevo las consultas
        misiones = getAllData('select * from mision ORDER BY codigo')
    return render_template("misiones.html", misiones = misiones)


'''tabla de aves y familia'''

@app.route('/aves', methods=['GET','POST'])
def aves():

    aves = getAllData('select * from ave ORDER BY codigo')
    familias = getAllData('select * from familia ORDER BY codigo')

    if request.method == 'POST':
        id = request.form.get("idmave")
        print(id)
        nomCo = request.form.get("nomCo")
        print(nomCo)
        nomCi = request.form.get("nomCi")
        print(nomCi)
        genero = request.form.get("genero")
        print(genero)
        especie = request.form.get("especie")
        print(especie)
        descripcion = request.form.get("descripcion")
        print(descripcion)
        orden = request.form.get("orden")
        print(orden)
        colores = request.form.get("colores")
        print(colores)
        idFamiliaAve = request.form.get("idFamiliaAve")
        print(idFamiliaAve)
        codigo = request.form.get("idaveEl")
        print(codigo)
        valor = request.form.get("valor")
        valorUno = request.form.get("valorUno")
        print(valor)
        if(valor is None):
            if(id!=''):
                print("actualizaremos")
                sql_update_query = """Update ave set nombre_comun = %s, nombre_cientifico = %s, genero= %s,
                especie = %s, descripcion = %s, orden= %s,
                colores_principales = %s, codigo_familia = %s where codigo = %s"""
                record_to_update = (nomCo, nomCi, genero,especie,descripcion,orden,colores,idFamiliaAve,id)
                insertData(sql_update_query,record_to_update, valorUno)

            else:
                print("insertaremos")
                postgres_insert_query = """ INSERT INTO ave (nombre_comun, nombre_cientifico, genero,
                especie,descripcion,orden,colores_principales,codigo_familia) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                record_to_insert = (nomCo, nomCi, genero,especie,descripcion,orden,colores,idFamiliaAve)
                insertData(postgres_insert_query,record_to_insert, valorUno)
        else:
            print(valor)
            sql_delete_query = """Delete from ave where codigo = %s"""
            record_to_delete = (codigo,)
            insertData(sql_delete_query,record_to_delete, valor) 
        
        #realizando de nuevo las consultas
        aves = getAllData('select * from ave ORDER BY codigo')
        familias = getAllData('select * from familia ORDER BY codigo')
    return render_template("aves.html", aves = aves, familias=familias)

@app.route('/familia', methods=['GET','POST'])
def familia():

    aves = getAllData('select * from ave ORDER BY codigo')
    familias = getAllData('select * from familia ORDER BY codigo')


    if request.method == 'POST':
        id = request.form.get("idfami")
        print(id)
        nombre = request.form.get("nombre")
        print(nombre)
        descripcion = request.form.get("descripcion")
        print(descripcion)
        codigo = request.form.get("idfamiEl")
        print(codigo)
        valor = request.form.get("valor")
        valorUno = request.form.get("valorUno")
        print(valor)
        if(valor is None):
            if(id!=''):
                print("actualizaremos")
                sql_update_query = """Update familia set nombre = %s, descripcion = %s where codigo = %s"""
                record_to_update = (nombre, descripcion, id)
                insertData(sql_update_query,record_to_update, valorUno)

            else:
                print("insertaremos")
                postgres_insert_query = """ INSERT INTO familia (nombre, descripcion) VALUES (%s,%s)"""
                record_to_insert = (nombre, descripcion)
                insertData(postgres_insert_query,record_to_insert, valorUno)
        else:
            print(valor)
            sql_delete_query = """Delete from familia where codigo = %s"""
            record_to_delete = (codigo,)
            insertData(sql_delete_query,record_to_delete, valor) 
        
        #realizando de nuevo las consultas
    aves = getAllData('select * from ave ORDER BY codigo')
    familias = getAllData('select * from familia ORDER BY codigo')
    return render_template("aves.html", aves = aves, familias=familias)