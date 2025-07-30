from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuarioModel import *

usuariosBP = Blueprint('usuarios', __name__)

# Ruta para guardar usuarios
@usuariosBP.route('/guardarUsuario', methods=['POST'])
def guardar():
    errores = {} 
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
            insertUsuario(nombre, correo, contrasena, telefono)
            flash('Usuario guardado en la BD')
            return redirect(url_for('dashboard.inicio'))
        
        except Exception as e:
            flash('Algo fallo:' + str(e))
            return redirect(url_for('dashboard.inicio'))
    
    # Si hay errores, redirigir con flash de errores
    for campo, mensaje in errores.items():
        flash(mensaje)
    return redirect(url_for('dashboard.inicio'))

# Ruta para cargar datos a modificar
@usuariosBP.route('/modificar_usuario/<int:id>')
def modificar(id):
    try:
        errores = session.get("errores", "")
        consultaId = getByIdUsuarios(id)
        return render_template('modificar_usuarios.html', nUsuario=consultaId)
        
    except Exception as e:
        print('Error en consulta: ' + str(e))
        errores = {'general': 'Hubo un problema cargando los datos'}
        return render_template('index.html',
                                errores=errores,
                                vista="",
                                usuarios=[],
                                administradores=[],
                                semillas=[],
                                tutoriales=[])
    finally:
        session.pop("vista_activa", None)
        session.pop("errores", None)
        session.pop("sobreescribirSemilla", None)

# Ruta para actualizar usuario
@usuariosBP.route('/actualizar_usuario', methods=['POST'])
def actualizar():
    errores = {}
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
            updateUsuario(idUpdate, nNombre, nCorreo, nContrasena, nTelefono)
            flash('Usuario actualizado correctamente')
            return redirect(url_for('dashboard.inicio'))
        
        except Exception as e:
            flash('Algo fallo:' + str(e))
            return redirect(url_for('dashboard.inicio'))
    
    # Si hay errores, redirigir con flash de errores
    for campo, mensaje in errores.items():
        flash(mensaje)
    return redirect(url_for('dashboard.inicio'))

# Ruta para eliminar usuario
@usuariosBP.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        softDeleteUsuario(id)
        flash('Usuario eliminado correctamente')
        return redirect(url_for('dashboard.inicio'))
        
    except Exception as e:
        flash('Error al eliminar: ' + str(e))
        return redirect(url_for('dashboard.inicio'))