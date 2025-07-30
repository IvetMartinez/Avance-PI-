from flask import Flask, jsonify, session
from flask_mysqldb import MySQL
import MySQLdb
from config import Config

mysql = MySQL()

def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    
    # Registro de blueprints
    from controllers.usuarioController import usuariosBP
    from controllers.administradorController import administradoresBP
    from controllers.semillaController import semillasBP
    from controllers.tutorialController import tutorialesBP
    from controllers.dashboardController import dashboardBP
    
    app.register_blueprint(dashboardBP)
    app.register_blueprint(usuariosBP)
    app.register_blueprint(administradoresBP)
    app.register_blueprint(semillasBP)
    app.register_blueprint(tutorialesBP)
    
    return app

app = Flask(__name__)

@app.before_request
def before_request():
    session.permanent = False

# Ruta para consultar la conexión a la base de datos
@app.route('/DBCheck')
def DB_check():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('Select 1')
        return jsonify({'status':'ok', 'message':'Conectado con exito'}), 200        
    except MySQLdb.MySQLError as e:
        return jsonify({'status':'error', 'message':str(e)}), 500  

# Ruta try-catch de posibles errores
@app.errorhandler(404)
def paginaNoE(e):
    return 'Cuidado: Error de capa 8! :c', 404

@app.errorhandler(405)
def metodoNoPermitido(e):
    return 'Revisa el metodo de envio de tu ruta (GET o POST)', 405

if __name__ == '__main__':
    app = createApp()
    app.run(port=3000, debug=True)