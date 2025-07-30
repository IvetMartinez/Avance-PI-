from flask import Blueprint, render_template, session
from models.usuarioModel import *
from models.administradorModel import *
from models.semillaModel import *
from models.tutorialModel import *

dashboardBP = Blueprint('dashboard', __name__)

# Ruta de inicio (dashboard principal)
@dashboardBP.route('/')
def inicio():
    try:
        errores = session.get("errores", "")
        vista = session.get("vista_activa", "")

        # Contadores para el dashboard
        contador_usuarios = getUsuariosCount()
        contador_administradores = getAdministradoresCount()
        contador_semillas = getSemillasCount()
        contador_tutoriales = getTutorialesCount()
        
        # Consultas para las tablas
        consultaUsuarios = getAllUsuarios() # usuarios
        consultaAdministradores = getAllAdministradores() # administradores
        consultaSemillas = getAllSemillas() # semillas
        consultaTutoriales = getAllTutoriales() # tutoriales
        
        # Datos para los selects (semillas)
        consultaVitaminas = getVitaminas()
        consultaMunicipios = getMunicipios()
        consultaTiposSemilla = getTiposSemilla()
        consultaFertilizantes = getFertilizantes()

        return render_template('index.html', 
                                errores=errores,
                                vista=vista,
                                # CONTADORES PARA EL DASHBOARD
                                total_usuarios=contador_usuarios,
                                total_administradores=contador_administradores,
                                total_semillas=contador_semillas,
                                total_tutoriales=contador_tutoriales,
                                # DATOS PARA LAS TABLAS
                                usuarios=consultaUsuarios,
                                administradores=consultaAdministradores, 
                                semillas=consultaSemillas, 
                                tutoriales=consultaTutoriales,
                                # DATOS PARA LOS SELECT
                                vitaminas=consultaVitaminas,
                                municipios=consultaMunicipios,
                                tipos_semilla=consultaTiposSemilla,
                                fertilizantes=consultaFertilizantes)
        
    except Exception as e:
        print('Error en algunas de las consultas: ' + str(e))
        errores = {'general': 'Hubo un problema cargando los datos'}
        
        return render_template('index.html',
                                errores=errores,
                                vista="",
                                # Contadores en 0 cuando hay error
                                total_usuarios=0,
                                total_administradores=0,
                                total_semillas=0,
                                total_tutoriales=0,
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
        session.pop("vista_activa", None)
        session.pop("errores", None)
        session.pop("sobreescribirSemilla", None)