from flask import Flask, jsonify, render_template, request,url_for, flash,redirect  #1 funcion para mandar llamar las vistas
from flask_mysqldb import MySQL
import MySQLdb

from flask import Flask

app = Flask (__name__)
 #definir variables
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="1111Ivet**"
app.config['MYSQL_DB']="PIQroHuerto"
app.config['MYSQL_PORT']=3306
app.secret_key ='mysecretkey'

mysql =MySQL(app)
@app.route('/')
def home():
    try:
        cursor= mysql.connection.cursor()
        cursor.execute('SELECT*FROM usuarios')
        consultatodo= cursor.fetchall()
        return render_template ('usuarios.html', errores ={},usuarios=consultatodo) #Regresa un render_template a la vista de formulario
        
    except Exception as e:
        print('Error al consultar todo: '+e)
        return render_template ('usuarios.html', errores ={},usuarios=[]) #Llega la respuesta vacía
    
        
    finally:
        cursor.close()  
        
 
    
    
    
    
    
 #ruta para probar la conección  a MYSQL
@app.route('/DBcheck')
def DBcheck():
    try:
        cursor=mysql.connection.cursor()
        cursor.execute('Select 1')
        return jsonify(  { 'status':'ok','message' : 'Conetactado con exito' }  ),200
    except MySQLdb.MySQLError as e:
         return jsonify( {'status': 'error', 'message' : str(e)}),500   
    
    
if __name__ == '__main__':
    app.run(port=3000, debug = True)
    #probar las rutas  con el parametro (nombre)
    #Hay que buscar el camino correcto y los posibles errores