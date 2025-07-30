from app import mysql

# Método para obtener administradores activos
def getAllAdministradores():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM administradores WHERE estado = 1')
    consultaTodo = cursor.fetchall()
    cursor.close()
    return consultaTodo

# Obtener administrador por id
def getByIdAdministradores(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM administradores WHERE id_admin = %s', (id,))
    consultaId = cursor.fetchone()
    cursor.close()
    return consultaId

# Método para insertar un administrador
def insertAdministrador(nombre, correo, contrasena, rol):
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO administradores(nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s)', 
                   (nombre, correo, contrasena, rol))
    mysql.connection.commit()
    cursor.close()

# Método para actualizar un administrador
def updateAdministrador(idUpdate, nNombre, nCorreo, nContrasena):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE administradores SET nombre = %s, correo = %s, contrasena = %s WHERE id_admin = %s',
                   (nNombre, nCorreo, nContrasena, idUpdate))
    mysql.connection.commit()
    cursor.close()

# Método para eliminar un administrador (soft delete)
def softDeleteAdministrador(id):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE administradores SET estado = 0 WHERE id_admin = %s', (id,))
    mysql.connection.commit()
    cursor.close()

# Método para obtener contador de administradores activos
def getAdministradoresCount():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM administradores WHERE estado = 1')
    contador = cursor.fetchone()[0]
    cursor.close()
    return contador