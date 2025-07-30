from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.semillaModel import *

semillasBP = Blueprint('semillas', __name__)

# Ruta para guardar semillas
@semillasBP.route('/agregar_semilla', methods=['POST'])
def agregar():
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
            insertSemilla(nombre_semilla, espacio_semilla, imagen_semilla, vitamina_semilla, municipio_semilla, tipo_semilla, fertilizante_semilla)
            flash("La semilla se guardó en la base de datos")
            return redirect(url_for('dashboard.inicio'))

        except Exception as e:
            errores["errorInterno"] = "Ocurrió un error, favor de intentarlo nuevamente más tarde"
            session["errores"] = errores
            return redirect(url_for('dashboard.inicio'))
    
    # Si hay errores, hacer flash y redirigir
    for campo, mensaje in errores.items():
        flash(mensaje)
    return redirect(url_for('dashboard.inicio'))

# Ruta para cargar datos a modificar
@semillasBP.route('/modificar_semilla/<int:id>')
def modificar(id):
    try:
        nSemilla = getByIdSemillas(id)
        
        # Consultas para los select
        consultaVitaminas = getVitaminas()
        consultaMunicipios = getMunicipios()
        consultaTiposSemilla = getTiposSemilla()
        consultaFertilizantes = getFertilizantes()
        
        return render_template('modificar_semilla.html', 
                                nSemilla=nSemilla, 
                                errores={},
                                vitaminas=consultaVitaminas,
                                municipios=consultaMunicipios,
                                tipos_semilla=consultaTiposSemilla,
                                fertilizantes=consultaFertilizantes)
        
    except Exception as e:
        flash('Algo fallo:' + str(e))
        return redirect(url_for('dashboard.inicio'))

# Ruta para actualizar semilla
@semillasBP.route('/actualizar_semilla', methods=['POST'])
def actualizar():
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
            updateSemilla(idUpdate, nnombre_semilla, nespacio_semilla, nimagen_semilla, nvitamina_semilla, nmunicipio_semilla, ntipo_semilla, nfertilizante_semilla)
            flash("La semilla se actualizó en la base de datos")
            return redirect(url_for('dashboard.inicio'))

        except Exception as e:
            errores["errorInterno"] = "Ocurrió un error, favor de intentarlo nuevamente más tarde"
            session["errores"] = errores
            return redirect(url_for('dashboard.inicio'))
    
    # Si hay errores, hacer flash y redirigir
    for campo, mensaje in errores.items():
        flash(mensaje)
    return redirect(url_for('dashboard.inicio'))

# Ruta para eliminar semilla
@semillasBP.route('/eliminar_semilla/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        softDeleteSemilla(id)
        flash('Semilla eliminada correctamente')
        return redirect(url_for('dashboard.inicio'))
        
    except Exception as e:
        flash('Error al eliminar: ' + str(e))
        return redirect(url_for('dashboard.inicio'))