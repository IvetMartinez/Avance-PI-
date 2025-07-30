from app import mysql

# Método para obtener semillas activas con joins
def getAllSemillas():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT 
            s.Clave_semilla,
            s.Nombre,
            s.Espacio,
            s.Imagen_URL,
            v.Nombre as Vitamina,
            m.Nombre as Municipio,
            ts.Nombre as Tipo_Semilla,
            f.Nombre as Fertilizante
        FROM semillas s
        LEFT JOIN Vitaminas v ON s.Clave_Vitamina = v.Clave_vitamina
        LEFT JOIN Municipios m ON s.Clave_municipio = m.Clave_municipio
        LEFT JOIN Tipo_semilla ts ON s.Clave_tipo = ts.Idtiposemilla
        LEFT JOIN Fertilizantes f ON s.Clave_fertilizante = f.Clave_fertilizante
        WHERE s.estado = 1
        ORDER BY s.Nombre
    ''')
    consultaTodo = cursor.fetchall()
    cursor.close()
    return consultaTodo

# Obtener semilla por id
def getByIdSemillas(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM semillas WHERE Clave_semilla = %s', (id,))
    consultaId = cursor.fetchone()
    cursor.close()
    return consultaId

# Método para insertar una semilla
def insertSemilla(nombre_semilla, espacio_semilla, imagen_semilla, vitamina_semilla, municipio_semilla, tipo_semilla, fertilizante_semilla):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Semillas(Nombre, Espacio, Imagen_URL, Clave_Vitamina, Clave_municipio, Clave_tipo, Clave_fertilizante) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (nombre_semilla, espacio_semilla, imagen_semilla, vitamina_semilla, municipio_semilla, tipo_semilla, fertilizante_semilla))
    mysql.connection.commit()
    cursor.close()

# Método para actualizar una semilla
def updateSemilla(idUpdate, nnombre_semilla, nespacio_semilla, nimagen_semilla, nvitamina_semilla, nmunicipio_semilla, ntipo_semilla, nfertilizante_semilla):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE semillas SET nombre = %s, espacio =%s, Imagen_URL = %s, clave_vitamina = %s, Clave_municipio =%s, Clave_tipo =%s, Clave_fertilizante = %s WHERE Clave_semilla = %s', 
                   (nnombre_semilla, nespacio_semilla, nimagen_semilla, nvitamina_semilla, nmunicipio_semilla, ntipo_semilla, nfertilizante_semilla, idUpdate))
    mysql.connection.commit()
    cursor.close()

# Método para eliminar una semilla (soft delete)
def softDeleteSemilla(id):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE semillas SET estado = 0 WHERE Clave_semilla = %s', (id,))
    mysql.connection.commit()
    cursor.close()

# Método para obtener contador de semillas activas
def getSemillasCount():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM semillas WHERE estado = 1')
    contador = cursor.fetchone()[0]
    cursor.close()
    return contador

# Métodos para obtener datos de los selects
def getVitaminas():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT Clave_vitamina, Nombre FROM Vitaminas ORDER BY Nombre')
    consultaVitaminas = cursor.fetchall()
    cursor.close()
    return consultaVitaminas

def getMunicipios():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT Clave_municipio, Nombre FROM Municipios ORDER BY Nombre')
    consultaMunicipios = cursor.fetchall()
    cursor.close()
    return consultaMunicipios

def getTiposSemilla():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT Idtiposemilla, Nombre FROM Tipo_semilla ORDER BY Nombre')
    consultaTiposSemilla = cursor.fetchall()
    cursor.close()
    return consultaTiposSemilla

def getFertilizantes():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT Clave_fertilizante, Nombre FROM Fertilizantes ORDER BY Nombre')
    consultaFertilizantes = cursor.fetchall()
    cursor.close()
    return consultaFertilizantes