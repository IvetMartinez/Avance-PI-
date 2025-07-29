import re
from flask import Flask, jsonify, render_template, request, url_for, flash, redirect, session
from flask_mysqldb import MySQL
import MySQLdb

app = Flask (__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Kesadilla94"
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
        
        # Contador de Usuarios Activos
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE estado = 1')
        contador_usuarios = cursor.fetchone()[0]
        
        # Contador de Administradores Activos
        cursor.execute('SELECT COUNT(*) FROM administradores WHERE estado = 1')
        contador_administradores = cursor.fetchone()[0]
        
        # Contador de Semillas Activas
        cursor.execute('SELECT COUNT(*) FROM semillas WHERE estado = 1')
        contador_semillas = cursor.fetchone()[0]
        
        # Contador de Tutoriales/Videos Activos
        cursor.execute('SELECT COUNT(*) FROM videos WHERE estado = 1')
        contador_tutoriales = cursor.fetchone()[0]
        
        # Consulta de Usuarios
        cursor.execute('SELECT * FROM usuarios where estado = 1')
        consultaUsuarios = cursor.fetchall()
        
        # Consulta de Administradores
        cursor.execute('SELECT * FROM administradores where estado = 1')
        consultaAdministradores = cursor.fetchall()
        
        # Consulta de Semillas
        cursor.execute('''
            SELECT 
                s.Clave_semilla,
                s.Nombre,
                s.Espacio,
                s.Imagen_URL,
                v.Nombre as Vitamina,
                m.Nombre as Municipio,
                ts.Nombre as Tipo_Semilla,
                f.Nombre as Fertilizante
            FROM semillas s
            LEFT JOIN Vitaminas v ON s.Clave_Vitamina = v.Clave_vitamina
            LEFT JOIN Municipios m ON s.Clave_municipio = m.Clave_municipio
            LEFT JOIN Tipo_semilla ts ON s.Clave_tipo = ts.Idtiposemilla
            LEFT JOIN Fertilizantes f ON s.Clave_fertilizante = f.Clave_fertilizante
            WHERE s.estado = 1
            ORDER BY s.Nombre
        ''')
        consultaSemillas = cursor.fetchall()
        # Consulta de Tutoriales
        cursor.execute('SELECT * FROM videos where estado = 1')
        consultaTutoriales = cursor.fetchall()
        # Consulta de Vitaminas
        cursor.execute('SELECT Clave_vitamina, Nombre FROM Vitaminas ORDER BY Nombre')
        consultaVitaminas = cursor.fetchall()
        
        # Consulta de Municipios
        cursor.execute('SELECT Clave_municipio, Nombre FROM Municipios ORDER BY Nombre')
        consultaMunicipios = cursor.fetchall()
        
        # Consulta de Tipos de Semilla
        cursor.execute('SELECT Idtiposemilla, Nombre FROM Tipo_semilla ORDER BY Nombre')
        consultaTiposSemilla = cursor.fetchall()
        
        # Consulta de Fertilizantes
        cursor.execute('SELECT Clave_fertilizante, Nombre FROM Fertilizantes ORDER BY Nombre')
        consultaFertilizantes = cursor.fetchall()

        return render_template('index.html', 
                                errores=errores,
                                vista=vista,
                                # CONTADORES PARA EL DASHBOARD
                                total_usuarios = contador_usuarios,
                                total_administradores = contador_administradores,
                                total_semillas = contador_semillas,
                                total_tutoriales = contador_tutoriales,
                                # DATOS PARA LAS TABLAS
                                usuarios = consultaUsuarios,
                                administradores = consultaAdministradores, 
                                semillas = consultaSemillas, 
                                tutoriales = consultaTutoriales,
                                # DATOS PARA LOS SELECT
                                vitaminas = consultaVitaminas,
                                municipios = consultaMunicipios,
                                tipos_semilla = consultaTiposSemilla,
                                fertilizantes = consultaFertilizantes)
        
    except Exception as e:
        # Aquí convertimos 'e' a cadena antes de usarlo
        print('Error en algunas de las consultas: ' + str(e))

        # Puedes enviar un mensaje de error a la plantilla si quieres mostrarlo
        errores['general'] = 'Hubo un problema cargando los datos'
        return render_template('index.html',
                                errores=errores,
                                vista="",
                                # Contadores en 0 cuando hay error
                                total_usuarios = 0,
                                total_administradores = 0,
                                total_semillas = 0,
                                total_tutoriales = 0,
                                # Listas vacías
                                usuarios=[],
                                administradores=[],
                                semillas=[],
                                tutoriales=[],
                                # Variables vacías para los select
                                vitaminas=[],
                                municipios=[],
                                tipos_semilla=[],
                                fertilizantes=[])

    finally:
        cursor.close()
        session.pop("vista_activa", None)
        session.pop("errores", None)
        session.pop("sobreescribirSemilla", None)


#Rutas para guardar usuarios, actualizarlos y eliminarlos
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
            
            
@app.route('/modificar_usuario/<int:id>')
def modificarUsuario(id):
    
    try:
        errores = session.get("errores", "")
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from usuarios where Idusuario = %s', (id,))
        consultaId = cursor.fetchone()
        return render_template ('modificar_usuarios.html', nUsuario = consultaId)
        
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
        
@app.route('/actualizar_usuario', methods=['POST'])
def actualizarUsuario():
    errores= {}
    idUpdate = request.form.get('idUsuario', '').strip()
    nNombre = request.form.get('ntxtNombre', '').strip()
    nCorreo = request.form.get('ntxtCorreo', '').strip()
    nContrasena = request.form.get('ntxtContrasena', '').strip()
    nTelefono = request.form.get('ntxtTelefono', '').strip()
    
    
    if not nNombre:
        errores['ntxtNombre'] = 'Nombre del usuario Obligatorio'
        
    if not nCorreo:
        errores['ntxtCorreo'] = 'Correo es Obligatorio'
    
    if not nContrasena:
        errores['ntxtContrasena'] = 'Contraseña obligatoria'
    
    if not nTelefono:
        errores['ntxtTelefono'] = 'Teléfono obligatorio'

    if not errores:
        try:
            cursor= mysql.connection.cursor()
            cursor.execute('update usuarios set Nombre = %s, Email = %s, Contrasena = %s, Telefono = %s where Idusuario = %s',(nNombre, nCorreo,nContrasena, nTelefono, idUpdate))
            mysql.connection.commit()
            flash('Usuario actuzalizado correctamente')
            return redirect(url_for('Inicio'))
        
        except Exception as e:
            mysql.connection.rollback() 
            flash('Algo fallo:'+str(e))
            return  redirect(url_for('Inicio'))
        
        finally:
            cursor.close()
            
@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminarUsuario(id):
    
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE usuarios SET estado = 0 WHERE Idusuario = %s', (id,))
        mysql.connection.commit()
        flash('Usuario eliminado correctamente')
        return redirect(url_for('Inicio'))
        
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al eliminar: '+ str(e))
        return render_template('index.html')
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
            cursor.execute('INSERT INTO administradores(nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s)', (nombre, correo, contrasena, rol))
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
    

@app.route('/modificar_admin/<int:id>')
def modificarAdmin(id):
    
    try:
        errores = session.get("errores", "")
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from administradores where id_admin = %s', (id,))
        consultaId = cursor.fetchone()
        return render_template ('modificar_admins.html', nAdmin = consultaId)
        
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

@app.route('/actualizar_admin', methods=['POST'])
def actualizarAdmin():
    errores = {}
    idUpdate = request.form.get('idAdmin', '').strip()
    nNombre = request.form.get('ntxtNombre', '').strip()
    nCorreo = request.form.get('ntxtCorreo', '').strip()
    nContrasena = request.form.get('ntxtContrasena', '').strip()
    
    
    if not nNombre:
        errores['ntxtNombreAdmin'] = 'Nombre del administrador obligatorio'
    
    if not nCorreo:
        errores['ntxtCorreoAdmin'] = 'Correo electrónico obligatorio'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', nCorreo):
        errores['ntxtCorreo'] = 'Formato de correo inválido'
    
    if not nContrasena:
        errores['ntxtContrasenaAdmin'] = 'Contraseña obligatoria'
    elif len(nContrasena) < 8:
        errores['ntxtContrasenaAdmin'] = 'La contraseña debe tener al menos 8 caracteres'
    
    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('update administradores set nombre = %s, correo = %s, contrasena = %s where id_admin = %s',
                        (nNombre, nCorreo, nContrasena, idUpdate))
            mysql.connection.commit()
            flash('Administrador Actualizado')
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
    
@app.route('/eliminar_admin/<int:id>', methods=['POST'])
def eliminarAdmin(id):
    
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE administradores SET estado = 0 WHERE id_admin = %s', (id,))
        mysql.connection.commit()
        flash('Administrador eliminado correctamente')
        return redirect(url_for('Inicio'))
        
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al eliminar: '+ str(e))
        return render_template('index.html')
    finally:
        cursor.close()




@app.route("/agregar_semilla", methods=["POST"])
def agregarSemilla():
    
        session["vista_activa"] = "semillas"
        errores = {}

        nombre_semilla = request.form.get("nombre_semilla", "").strip().title()
        espacio_semilla = request.form.get("espacio", "").strip()
        imagen_semilla = request.form.get("imagen_semilla", "").strip()
        vitamina_semilla = request.form.get("vitamina", "").strip()
        municipio_semilla = request.form.get("municipio", "").strip()
        tipo_semilla = request.form.get("tipo_semilla", "").strip()
        fertilizante_semilla = request.form.get("fertilizante", "").strip()

        if not nombre_semilla:
            errores['nombre_semilla'] = 'Nombre de la semilla obligatoria'
        if not espacio_semilla:
            errores['espacio'] = 'Espacio de la semilla obligatoria'
        if not imagen_semilla:
            errores['imagen_semilla'] = 'Es necesario agregar una imagen'
        if not vitamina_semilla:
            errores['vitamina'] = 'Tipo de vitamina requerido'
        if not municipio_semilla:
            errores['municipio'] = 'Municipio requerido'
        if not tipo_semilla:
            errores['tipo_semilla'] = 'Tipo de semilla obligatoria'
        if not fertilizante_semilla:
            errores['fertilizante'] = 'Tipo de fertilizante obligatorio' 
        
        if not errores:
            try:   
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO Semillas(Nombre, Espacio, Imagen_URL, Clave_Vitamina, Clave_municipio, Clave_tipo, Clave_fertilizante) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre_semilla, espacio_semilla, imagen_semilla, vitamina_semilla, municipio_semilla, tipo_semilla, fertilizante_semilla))
                mysql.connection.commit()
                flash("La semilla se guardó en la base de datos")
                return render_template('index.html', errores=errores)

            except Exception as e:
                errores["errorInterno"] = "Ocurrió un error, favor de intentarlo nuevamente más tarde"
                session["errores"] = errores
                return render_template('index.html', errores=errores)
            finally:
                cursor.close()
        
        return render_template('index.html', errores = errores)
    
    
@app.route('/modificar_semilla/<int:id>')
def modificarSemilla(id):
    
    try:
        cursor = mysql.connection.cursor()
        
        # Consulta de la semilla específica
        cursor.execute('select * from semillas where Clave_semilla = %s', (id,))
        nSemilla = cursor.fetchone()
        
        # Consultas para los select (mismas que en la ruta principal)
        cursor.execute('SELECT Clave_vitamina, Nombre FROM Vitaminas ORDER BY Nombre')
        consultaVitaminas = cursor.fetchall()
        
        cursor.execute('SELECT Clave_municipio, Nombre FROM Municipios ORDER BY Nombre')
        consultaMunicipios = cursor.fetchall()
        
        cursor.execute('SELECT Idtiposemilla, Nombre FROM Tipo_semilla ORDER BY Nombre')
        consultaTiposSemilla = cursor.fetchall()
        
        cursor.execute('SELECT Clave_fertilizante, Nombre FROM Fertilizantes ORDER BY Nombre')
        consultaFertilizantes = cursor.fetchall()
        
        return render_template('modificar_semilla.html', 
                                nSemilla = nSemilla, 
                                errores = {},
                                vitaminas = consultaVitaminas,
                                municipios = consultaMunicipios,
                                tipos_semilla = consultaTiposSemilla,
                                fertilizantes = consultaFertilizantes)
        
    except Exception as e:
        mysql.connection.rollback() 
        flash('Algo fallo:'+ str(e))
        return  redirect(url_for('Inicio'))
        
    finally:
        cursor.close()
    
@app.route("/actualizar_semilla", methods=["POST"])
def actualizarSemilla():
        session["vista_activa"] = "semillas"
        errores = {}
        idUpdate = request.form.get('idSemilla', '').strip()
        nnombre_semilla = request.form.get("nnombre_semilla", "").strip().title()
        nespacio_semilla = request.form.get("nespacio", "").strip()
        nimagen_semilla = request.form.get("nimagen_semilla", "").strip()
        nvitamina_semilla = request.form.get("nvitamina", "").strip()
        nmunicipio_semilla = request.form.get("nmunicipio", "").strip()
        ntipo_semilla = request.form.get("ntipo_semilla", "").strip()
        nfertilizante_semilla = request.form.get("nfertilizante", "").strip()

        if not nnombre_semilla:
            errores['nombre_semilla'] = 'Nombre de la semilla obligatoria'
        if not nespacio_semilla:
            errores['espacio'] = 'Espacio de la semilla obligatoria'
        if not nimagen_semilla:
            errores['imagen_semilla'] = 'Es necesario agregar una imagen'
        if not nvitamina_semilla:
            errores['vitamina'] = 'Tipo de vitamina requerido'
        if not nmunicipio_semilla:
            errores['municipio'] = 'Municipio requerido'
        if not ntipo_semilla:
            errores['tipo_semilla'] = 'Tipo de semilla obligatoria'
        if not nfertilizante_semilla:
            errores['fertilizante'] = 'Tipo de fertilizante obligatorio' 
        
        if not errores:
            try:   
                cursor = mysql.connection.cursor()
                cursor.execute('update semillas set nombre = %s, espacio =%s, Imagen_URL = %s, clave_vitamina = %s, Clave_municipio =%s, Clave_tipo =%s, Clave_fertilizante = %s where Clave_semilla = %s', (nnombre_semilla, nespacio_semilla, nimagen_semilla, nvitamina_semilla, nmunicipio_semilla, ntipo_semilla, nfertilizante_semilla, idUpdate))
                mysql.connection.commit()
                flash("La semilla se guardó en la base de datos")
                return redirect(url_for('Inicio'))

            except Exception as e:
                errores["errorInterno"] = "Ocurrió un error, favor de intentarlo nuevamente más tarde"
                session["errores"] = errores
                return render_template('modificar_semilla.html', errores=errores)
            finally:
                cursor.close()
        
        return render_template('index.html', errores = errores)
    
@app.route('/eliminar_semilla/<int:id>', methods=['POST'])
def eliminarSemilla(id):
    
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE semillas SET estado = 0 WHERE Clave_semilla = %s', (id,))
        mysql.connection.commit()
        flash('Semilla eliminada correctamente')
        return redirect(url_for('Inicio'))
        
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al eliminar: '+ str(e))
        return render_template('index.html')
    finally:
        cursor.close()


    
    
#TERMINAR LA SECCIÓN DE CRUD DE LOS TUTORIALES
@app.route('/guardarTutorial', methods=['POST'])
def guardarTutorial():
    errores= {} 
    nombre = request.form.get('nombre_video', '').strip()
    descripcion = request.form.get('descripcion_video', '').strip()
    URL = request.form.get('URL_video', '').strip()
    
    
    
    if not nombre:
        errores['nombre_video'] = 'Nombre del video Obligatorio'
        
    if not descripcion:
        errores['descripcion_video'] = 'Descripción del video es obligatoria'
    
    if not URL:
        errores['URL_video'] = 'Necesitas colocar '
    
    

    if not errores:
        try:
            cursor= mysql.connection.cursor()
            cursor.execute('insert into videos(nombre, descripción, URL) values(%s,%s,%s)',(nombre, descripcion, URL))
            mysql.connection.commit()
            flash('Video guardado exitosamente')
            return redirect(url_for('Inicio'))
        
        except Exception as e:
            mysql.connection.rollback() 
            flash('Algo fallo:'+str(e))
            return  redirect(url_for('Inicio'))
        
        finally:
            cursor.close()
            
    return render_template('index.html', errores=errores)
@app.route('/modificar_tutorial/<int:id>')
def modificarTutorial(id):
    
    try:
        errores = session.get("errores", "")
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from videos where Clave_video = %s', (id,))
        consultaId = cursor.fetchone()
        return render_template ('modificar_tutoriales.html', nTuto = consultaId)
        
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
        
@app.route('/actualizar_tutorial', methods=['POST'])
def actualizarTutorial():
    errores= {}
    idUpdate = request.form.get('idTutorial', '').strip()
    nnombre = request.form.get('nnombre_video', '').strip()
    ndescripcion = request.form.get('ndescripcion_video', '').strip()
    nURL = request.form.get('nURL_video', '').strip()
    
    
    
    if not nnombre:
        errores['nnombre_video'] = 'Nombre del video Obligatorio'
        
    if not ndescripcion:
        errores['ndescripcion_video'] = 'Descripción del video es obligatoria'
    
    if not nURL:
        errores['nURL_video'] = 'Necesitas ingresar una URL'
    
    

    if not errores:
        try:
            cursor= mysql.connection.cursor()
            cursor.execute('update videos set Nombre = %s, Descripción = %s, URL = %s where Clave_video = %s',(nnombre, ndescripcion, nURL, idUpdate))
            mysql.connection.commit()
            flash('Tutorial actuzalizado correctamente')
            return redirect(url_for('Inicio'))
        
        except Exception as e:
            mysql.connection.rollback() 
            flash('Algo fallo:'+str(e))
            return  redirect(url_for('Inicio'))
        
        finally:
            cursor.close()
            
@app.route('/eliminar_tutorial/<int:id>', methods=['POST'])
def eliminarTutorial(id):
    
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE videos SET estado = 0 WHERE Clave_video = %s', (id,))
        mysql.connection.commit()
        flash('Tutorial eliminado correctamente')
        return redirect(url_for('Inicio'))
        
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al eliminar: '+ str(e))
        return render_template('index.html')
    finally:
        cursor.close()



if __name__ == '__main__':
    app.run(port=3000, debug=True)