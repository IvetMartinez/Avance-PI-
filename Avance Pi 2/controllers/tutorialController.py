from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.tutorialModel import *

tutorialesBP = Blueprint('tutoriales', __name__)

# Ruta para guardar tutoriales
@tutorialesBP.route('/guardarTutorial', methods=['POST'])
def guardar():
    errores = {} 
    nombre = request.form.get('nombre_video', '').strip()
    descripcion = request.form.get('descripcion_video', '').strip()
    URL = request.form.get('URL_video', '').strip()
    
    if not nombre:
        errores['nombre_video'] = 'Nombre del video Obligatorio'
    if not descripcion:
        errores['descripcion_video'] = 'Descripción del video es obligatoria'
    if not URL:
        errores['URL_video'] = 'Necesitas colocar una URL válida'

    if not errores:
        try:
            insertTutorial(nombre, descripcion, URL)
            flash('Video guardado exitosamente')
            return redirect(url_for('dashboard.inicio'))
        
        except Exception as e:
            flash('Algo fallo:' + str(e))
            return redirect(url_for('dashboard.inicio'))
    
    # Si hay errores, hacer flash y redirigir
    for campo, mensaje in errores.items():
        flash(mensaje)
    return redirect(url_for('dashboard.inicio'))

# Ruta para cargar datos a modificar
@tutorialesBP.route('/modificar_tutorial/<int:id>')
def modificar(id):
    try:
        errores = session.get("errores", "")
        consultaId = getByIdTutoriales(id)
        return render_template('modificar_tutoriales.html', nTuto=consultaId)
        
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

# Ruta para actualizar tutorial
@tutorialesBP.route('/actualizar_tutorial', methods=['POST'])
def actualizar():
    errores = {}
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
            updateTutorial(idUpdate, nnombre, ndescripcion, nURL)
            flash('Tutorial actualizado correctamente')
            return redirect(url_for('dashboard.inicio'))
        
        except Exception as e:
            flash('Algo fallo:' + str(e))
            return redirect(url_for('dashboard.inicio'))
    
    # Si hay errores, hacer flash y redirigir
    for campo, mensaje in errores.items():
        flash(mensaje)
    return redirect(url_for('dashboard.inicio'))

# Ruta para eliminar tutorial
@tutorialesBP.route('/eliminar_tutorial/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        softDeleteTutorial(id)
        flash('Tutorial eliminado correctamente')
        return redirect(url_for('dashboard.inicio'))
        
    except Exception as e:
        flash('Error al eliminar: ' + str(e))
        return redirect(url_for('dashboard.inicio'))