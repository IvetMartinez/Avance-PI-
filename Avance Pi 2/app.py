from flask import Flask, jsonify, render_template, request, url_for, flash, redirect, session
from flask_mysqldb import MySQL
import MySQLdb

app = Flask (__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "123456"
app.config['MYSQL_DB'] = "QroHuerto"
#app.config['MYSQL_PORT'] = 3306
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

@app.before_request
def before_request():
    session.permanent = False

#ruta para consultar la conexión a la base de datos
@app.route('/DBCheck')
def DB_check():
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('Select 1')
        return jsonify({'status':'ok', 'message':'Conectado con exito'}), 200        
        
        
    except MySQLdb.MySQLError as e:
        return jsonify({'status':'error', 'message':str(e)}), 500  
        

        
#ruta try-catch de posibles errores
@app.errorhandler(404)
def paginaNoE(e):
    return 'Cuidado: Error de capa 8! :c', 404
    

@app.errorhandler(405)
def metodoNoPermitido(e):
    return 'Revisa el meotodo de envio de tu ruta (GET o POST)', 405

#session.clear()

#Ruta de inicio
@app.route('/')
def Inicio():
    
    errores = session.get("errores", "")

    
    #En este ruta irán todas las consultas de los 4 formularios
    #Porque todos los formualarios están en un sólo archivo html
    #Se deben insertar las 4 consultas en el mismo try-catch para evitar hacer varios html
    
    
    #try-catch de Formularios
    
    try:
        
        #Inicio del cursor
        cursor = mysql.connection.cursor()
        
        #Consulta de Usuarios
        cursor.execute('select * from usuarios')
        consultaUsuarios = cursor.fetchall()
        
        #Consulta de Administradores
        cursor.execute('select * from administradores')
        consultaAdministradores = cursor.fetchall()
        
        #Consulta de Semillas
        cursor.execute('select * from semillas')
        consultaSemillas = cursor.fetchall()
        
        #Consulta de Tutoriales
        cursor.execute('select * from videos')
        consultaTutoriales = cursor.fetchall()
        
        
        
        
        return render_template('index.html', 
                                errores=errores,
                                usuarios = consultaUsuarios,
                                administradores = consultaAdministradores, 
                                semillas = consultaSemillas, 
                                tutoriales = consultaTutoriales)
        
    except Exception as e:
        
        
        print('Error en algunas de las consultas: ' + e)
        return render_template('index.html',
                                errores={},
                                usuarios = {},
                                administradores = {}, 
                                semillas = {},
                                tutoriales = {})
        
    finally:
        cursor.close()

@app.route("/agregar_semilla", methods=["POST"])
def agregarSemilla():
    try:
        session["vista_activa"] = "semillas"
        errores = {}

        nombre_semilla = request.form.get("nombre_semilla", "").strip().title()
        espacio_semilla = request.form.get("espacio", "").strip()
        imagen_semilla = request.form.get("imagen_semilla", "").strip()
        vitamina_semilla = request.form.get("vitamina", "").strip()
        municipio_semilla = request.form.get("municipio", "").strip()
        tipo_semilla = request.form.get("tipo_semilla", "").strip()
        fertilizante_semilla = request.form.get("fertilizante", "").strip()

        if not nombre_semilla or not espacio_semilla or not imagen_semilla or not vitamina_semilla or not municipio_semilla or not tipo_semilla or not fertilizante_semilla:
            errores["camposVacios"] = "No se pueden dejar campos vacíos"
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT 1 FROM Semillas WHERE Nombre = %s", (nombre_semilla,))
            semillaDuplicada = cursor.fetchone()
            if not semillaDuplicada:
                cursor.execute("INSERT INTO Semillas(Nombre, Espacio, Imagen_URL, Clave_Vitamina, Clave_municipio, Clave_tipo, Clave_fertilizante) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre_semilla, espacio_semilla, imagen_semilla, vitamina_semilla, municipio_semilla, tipo_semilla, fertilizante_semilla))
                mysql.connection.commit()
                flash("La semilla se guardó en la base de datos")
                return redirect(url_for("Inicio"))
            else:
                lista_valores = [nombre_semilla, espacio_semilla, imagen_semilla, vitamina_semilla, municipio_semilla, tipo_semilla, fertilizante_semilla]
                errores["semillaDuplicada"] = "Ya existe una semilla bajo el mismo nombre, ¿deseas sobreescribir su información?"
                session["sobreescribirSemilla"] = lista_valores
        return render_template("index.html", errores = errores)

    except Exception as e:
        errores["errorInterno"] = "Ocurrió un error, favor de intentarlo nuevamente más tarde"
        return redirect(url_for("Inicio"))
    finally:
        cursor.close()

@app.route("/sobreescribir_semilla", methods=["POST"])
def sobreescribirSemilla():
    try:
        errores = {}

        nombre, espacio, imagen, vitamina, municipio, tipo, fertilizante = session.get("sobreescribirSemilla", "")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Clave_semilla FROM Semillas WHERE Nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        id_semilla = resultado[0]
        cursor.execute("UPDATE Semillas SET Nombre = %s, Espacio = %s, Imagen_URL = %s, Clave_Vitamina = %s, Clave_municipio = %s, Clave_tipo = %s, Clave_fertilizante = %s WHERE Clave_semilla = %s", (nombre, espacio, imagen, vitamina, municipio, tipo, fertilizante, id_semilla))
        mysql.connection.commit()
        flash("La semilla se guardó en la base de datos")
        return redirect(url_for("Inicio"))
    except Exception as e:
        errores["errorInterno"] = "Ocurrió un error, favor de intentarlo nuevamente más tarde"
        session["errores"] = errores
        return redirect(url_for("Inicio"))
    finally:
        cursor.close()

if __name__ == '__main__':
    
    app.run(port=3000, debug = True)