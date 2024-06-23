import sqlite3

#FUNCIÓN PARA CONECTAR LA BD
def conectar_bd(nombre_bd):
    """Conecta a la base de datos SQLite y devuelve la conexión y el cursor."""
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()
    return conn, cursor

#FUNCIÓN PARA CREAR LAS TABLAS DE LOS ACTORES
def crear_tablas(cursor):
    #Crear la tabla director
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS director (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
   
        
    )
    ''')
    #Crear la tabla supervisor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS supervisor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        director_id INTEGER,
        FOREIGN KEY(director_id) REFERENCES director(id)
    )
    ''')
    #Creación de la tabla profesor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profesor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        supervisor_id INTEGER,
        FOREIGN KEY(supervisor_id) REFERENCES supervisor(id)
    )
    ''')
    #Creación de la tabla alumno
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alumno (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    ''')
    #Creación de la tabla grupo
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grupo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    ''')
    #Complementos de la tabla grupo
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profesor_grupo (
        profesor_id INTEGER,
        grupo_id INTEGER,
        PRIMARY KEY (profesor_id, grupo_id),
        FOREIGN KEY (profesor_id) REFERENCES profesor(id),
        FOREIGN KEY (grupo_id) REFERENCES grupo(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alumno_grupo (
        alumno_id INTEGER,
        grupo_id INTEGER,
        PRIMARY KEY (alumno_id, grupo_id),
        FOREIGN KEY (alumno_id) REFERENCES alumno(id),
        FOREIGN KEY (grupo_id) REFERENCES grupo(id)
    )
    ''')

# Función para insertar un director
def insertar_director(cursor, nombre_director):
    cursor.execute('INSERT INTO director (nombre) VALUES (?)', (nombre_director,))
    return cursor.lastrowid

# Función para insertar un supervisor asociado a un director específico
def insertar_supervisor(cursor, nombre_supervisor, director_id):
    cursor.execute('INSERT INTO supervisor (nombre, director_id) VALUES (?, ?)', (nombre_supervisor, director_id))
    return cursor.lastrowid

# Función para insertar un profesor asociado a un supervisor específico
def insertar_profesor(cursor, nombre_profesor, supervisor_id):
    cursor.execute('INSERT INTO profesor (nombre, supervisor_id) VALUES (?, ?)', (nombre_profesor, supervisor_id))
    return cursor.lastrowid

# Función para insertar un alumno
def insertar_alumno(cursor, nombre_alumno):
    cursor.execute('INSERT INTO alumno (nombre) VALUES (?)', (nombre_alumno,))
    return cursor.lastrowid

# Función para insertar un grupo
def insertar_grupo(cursor, nombre_grupo):
    cursor.execute('INSERT INTO grupo (nombre) VALUES (?)', (nombre_grupo,))
    return cursor.lastrowid

# Función para asignar un profesor a un grupo
def asignar_profesor_a_grupo(cursor, profesor_id, grupo_id):
    cursor.execute('INSERT INTO profesor_grupo (profesor_id, grupo_id) VALUES (?, ?)', (profesor_id, grupo_id))

# Función para asignar un alumno a un grupo
def asignar_alumno_a_grupo(cursor, alumno_id, grupo_id):
    cursor.execute('INSERT INTO alumno_grupo (alumno_id, grupo_id) VALUES (?, ?)', (alumno_id, grupo_id))
