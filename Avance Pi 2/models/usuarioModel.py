from app import mysql

# Método para obtener usuarios activos
def getAllUsuarios():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE estado = 1')
    consultaTodo = cursor.fetchall()
    cursor.close()
    return consultaTodo

# Obtener usuario por id
def getByIdUsuarios(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE Idusuario = %s', (id,))
    consultaId = cursor.fetchone()
    cursor.close()
    return consultaId

# Método para insertar un usuario
def insertUsuario(nombre, correo, contrasena, telefono):
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO usuarios(nombre, email, contrasena, telefono) VALUES(%s, %s, %s, %s)', 
                   (nombre, correo, contrasena, telefono))
    mysql.connection.commit()
    cursor.close()

# Método para actualizar un usuario
def updateUsuario(idUpdate, nNombre, nCorreo, nContrasena, nTelefono):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE usuarios SET Nombre = %s, Email = %s, Contrasena = %s, Telefono = %s WHERE Idusuario = %s',
                   (nNombre, nCorreo, nContrasena, nTelefono, idUpdate))
    mysql.connection.commit()
    cursor.close()

# Método para eliminar un usuario (soft delete)
def softDeleteUsuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE usuarios SET estado = 0 WHERE Idusuario = %s', (id,))
    mysql.connection.commit()
    cursor.close()

# Método para obtener contador de usuarios activos
def getUsuariosCount():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE estado = 1')
    contador = cursor.fetchone()[0]
    cursor.close()
    return contador