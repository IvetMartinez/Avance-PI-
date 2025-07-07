import re
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
    return 'Revisa el metodo de envio de tu ruta (GET o POST)', 405

#session.clear()

#Ruta de inicio
@app.route('/')
def Inicio():
    
    #En este ruta irán todas las consultas de los 4 formularios
    #Porque todos los formualarios están en un sólo archivo html
    #Se deben insertar las 4 consultas en el mismo try-catch para evitar hacer varios html
    
    
    #try-catch de Formularios
    

    try:
        errores = session.get("errores", "")
        vista = session.get("vista_activa", "")

        # Inicio del cursor
        cursor = mysql.connection.cursor()
        
        # Consulta de Usuarios
        cursor.execute('SELECT * FROM usuarios')
        consultaUsuarios = cursor.fetchall()
        
        # Consulta de Administradores
        cursor.execute('SELECT * FROM administradores')
        consultaAdministradores = cursor.fetchall()
        
        # Consulta de Semillas
        cursor.execute('SELECT * FROM semillas')
        consultaSemillas = cursor.fetchall()
        
        # Consulta de Tutoriales
        cursor.execute('SELECT * FROM videos')
        consultaTutoriales = cursor.fetchall()

        return render_template('index.html', 
                                errores=errores,
                                vista=vista,
                                usuarios = consultaUsuarios,
                                administradores = consultaAdministradores, 
                                semillas = consultaSemillas, 
                                tutoriales = consultaTutoriales)
        
    except Exception as e:
        # Aquí convertimos 'e' a cadena antes de usarlo
        print('Error en algunas de las consultas: ' + str(e))

        # Puedes enviar un mensaje de error a la plantilla si quieres mostrarlo
        errores['general'] = 'Hubo un problema cargando los datos'
        return render_template('index.html',
                               errores=errores,
                               vista="",
                               usuarios=[],  # listas vacías
                               administradores=[],
                               semillas=[],
                               tutoriales=[])

    finally:
        cursor.close()
        session.pop("vista_activa", None)
        session.pop("errores", None)
        session.pop("sobreescribirSemilla", None)

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
        return render_template('index.html', errores=errores)

    except Exception as e:
        errores["errorInterno"] = "Ocurrió un error, favor de intentarlo nuevamente más tarde"
        session["errores"] = errores
        return render_template('index.html', errores=errores)
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
        return render_template('index.html', errores=errores)
    finally:
        cursor.close()
    
    
    
@app.route('/guardarUsuario', methods=['POST'])
def guardarusuario():
    errores= {} 
    nombre = request.form.get('txtNombre', '').strip()
    correo = request.form.get('txtCorreo', '').strip()
    contrasena = request.form.get('txtContrasena', '').strip()
    telefono = request.form.get('txtTelefono', '').strip()
    
    
    if not nombre:
        errores['txtNombre'] = 'Nombre del usuario Obligatorio'
        
    if not correo:
        errores['txtCorreo'] = 'Correo es Obligatorio'
    
    if not contrasena:
        errores['txtContrasena'] = 'Contraseña obligatoria'
    
    if not telefono:
        errores['txtTelefono'] = 'Teléfono obligatorio'

    if not errores:
        try:
            cursor= mysql.connection.cursor()
            cursor.execute('insert into usuarios(nombre,email,contrasena,telefono) values(%s,%s,%s,%s)',(nombre, correo,contrasena, telefono))
            mysql.connection.commit()
            flash('Usuario guardado en la BD')
            return redirect(url_for('Inicio'))
        
        except Exception as e:
            mysql.connection.rollback() 
            flash('Algo fallo:'+str(e))
            return  redirect(url_for('Inicio'))
        
        finally:
            cursor.close()
                
@app.route('/guardarAdmin', methods=['POST'])
def guardarAdmin():
    errores = {}
    nombre = request.form.get('txtNombre', '').strip()
    correo = request.form.get('txtCorreo', '').strip()
    contrasena = request.form.get('txtContrasena', '').strip()
    rol = request.form.get('txtRol', '').strip() or 'editor'
    
    if not nombre:
        errores['txtNombreAdmin'] = 'Nombre del administrador obligatorio'
    
    if not correo:
        errores['txtCorreoAdmin'] = 'Correo electrónico obligatorio'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
        errores['txtCorreo'] = 'Formato de correo inválido'
    
    if not contrasena:
        errores['txtContrasenaAdmin'] = 'Contraseña obligatoria'
    elif len(contrasena) < 8:
        errores['txtContrasenaAdmin'] = 'La contraseña debe tener al menos 8 caracteres'
    
    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO administradores(nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s)',
                         (nombre, correo, contrasena, rol))
            mysql.connection.commit()
            flash('Administrador guardado en la BD')
            return redirect(url_for('Inicio'))
        
        except Exception as e:
            mysql.connection.rollback()
            flash('Algo falló: ' + str(e))
            return redirect(url_for('Inicio'))
        
        finally:
            cursor.close()
    
    else:
        # Aquí está la corrección: manejar el caso cuando hay errores
        # Puedes hacer flash de los errores y redirigir, o renderizar un template
        for campo, mensaje in errores.items():
            flash(mensaje)
        return redirect(url_for('Inicio'))  # O el template que corresponda
       

if __name__ == '__main__':
    app.run(port=3000, debug=True)