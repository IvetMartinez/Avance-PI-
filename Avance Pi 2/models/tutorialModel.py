from app import mysql

# Método para obtener tutoriales activos
def getAllTutoriales():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM videos WHERE estado = 1')
    consultaTodo = cursor.fetchall()
    cursor.close()
    return consultaTodo

# Obtener tutorial por id
def getByIdTutoriales(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM videos WHERE Clave_video = %s', (id,))
    consultaId = cursor.fetchone()
    cursor.close()
    return consultaId

# Método para insertar un tutorial
def insertTutorial(nombre, descripcion, URL):
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO videos(nombre, descripción, URL) VALUES(%s, %s, %s)', 
                   (nombre, descripcion, URL))
    mysql.connection.commit()
    cursor.close()

# Método para actualizar un tutorial
def updateTutorial(idUpdate, nnombre, ndescripcion, nURL):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE videos SET Nombre = %s, Descripción = %s, URL = %s WHERE Clave_video = %s',
                   (nnombre, ndescripcion, nURL, idUpdate))
    mysql.connection.commit()
    cursor.close()

# Método para eliminar un tutorial (soft delete)
def softDeleteTutorial(id):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE videos SET estado = 0 WHERE Clave_video = %s', (id,))
    mysql.connection.commit()
    cursor.close()

# Método para obtener contador de tutoriales activos
def getTutorialesCount():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM videos WHERE estado = 1')
    contador = cursor.fetchone()[0]
    cursor.close()
    return contador