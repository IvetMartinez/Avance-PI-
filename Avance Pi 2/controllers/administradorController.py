import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.administradorModel import *

administradoresBP = Blueprint('administradores', __name__)

# Ruta para guardar administradores
@administradoresBP.route('/guardarAdmin', methods=['POST'])
def guardar():
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
            insertAdministrador(nombre, correo, contrasena, rol)
            flash('Administrador guardado en la BD')
            return redirect(url_for('dashboard.inicio'))
        
        except Exception as e:
            flash('Algo falló: ' + str(e))
            return redirect(url_for('dashboard.inicio'))
    else:
        # Si hay errores, hacer flash de los errores y redirigir
        for campo, mensaje in errores.items():
            flash(mensaje)
        return redirect(url_for('dashboard.inicio'))

# Ruta para cargar datos a modificar
@administradoresBP.route('/modificar_admin/<int:id>')
def modificar(id):
    try:
        errores = session.get("errores", "")
        consultaId = getByIdAdministradores(id)
        return render_template('modificar_admins.html', nAdmin=consultaId)
        
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

# Ruta para actualizar administrador
@administradoresBP.route('/actualizar_admin', methods=['POST'])
def actualizar():
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
            updateAdministrador(idUpdate, nNombre, nCorreo, nContrasena)
            flash('Administrador Actualizado')
            return redirect(url_for('dashboard.inicio'))
        
        except Exception as e:
            flash('Algo falló: ' + str(e))
            return redirect(url_for('dashboard.inicio'))
    else:
        # Si hay errores, hacer flash de los errores y redirigir
        for campo, mensaje in errores.items():
            flash(mensaje)
        return redirect(url_for('dashboard.inicio'))

# Ruta para eliminar administrador
@administradoresBP.route('/eliminar_admin/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        softDeleteAdministrador(id)
        flash('Administrador eliminado correctamente')
        return redirect(url_for('dashboard.inicio'))
        
    except Exception as e:
        flash('Error al eliminar: ' + str(e))
        return redirect(url_for('dashboard.inicio'))