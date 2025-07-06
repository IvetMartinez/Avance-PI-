from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
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


#Ruta de inicio
@app.route('/')
def Inicio():
    
    
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
                                errores={},
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
    

if __name__ == '__main__':
    
    app.run(port=3000, debug = True)