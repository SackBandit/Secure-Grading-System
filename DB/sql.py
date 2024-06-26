from datetime import datetime
import sqlite3
import random

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
        nombre TEXT NOT NULL,
        clave_Privada TEXT,
        clave_Publica TEXT,
        iv TEXT
        
    )
    ''')
    #Crear la tabla supervisor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS supervisor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        director_id INTEGER,
        clave_Privada TEXT,
        clave_Publica TEXT,
        iv TEXT,
        FOREIGN KEY(director_id) REFERENCES director(id)
    )
    ''')
    #Creación de la tabla profesor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profesor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        supervisor_id INTEGER,
        clave_Privada TEXT,
        clave_Publica TEXT,
        iv TEXT,
        FOREIGN KEY(supervisor_id) REFERENCES supervisor(id)
    )
    ''')
    #Creación de la tabla alumno
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alumno (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        calificacion INTEGER
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

    # Crear la tabla comentarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comentarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profesor_id INTEGER,
        alumno_id INTEGER,
        grupo_id INTEGER,
        comentario TEXT NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (profesor_id) REFERENCES profesor(id),
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


#Funcion para generar reportes
def escribir_reporte(cursor, profesor_id, alumno_id, grupo_id, comentario, fecha):
    cursor.execute('''
    INSERT INTO comentarios (profesor_id, alumno_id, grupo_id, comentario, fecha)
    VALUES (?, ?, ?, ?, ?)''', (profesor_id, alumno_id, grupo_id, comentario, fecha))

def obtener_reportes(cursor):
    cursor.execute('''
    SELECT 
        comentarios.id,
        profesor.nombre AS nombre_profesor,
        alumno.nombre AS nombre_alumno,
        grupo.nombre AS nombre_grupo,
        reporte_comentarios.comentario,
        reporte_comentarios.fecha
    FROM 
        reporte_comentarios
    JOIN 
        profesor ON reporte_comentarios.profesor_id = profesor.id
    JOIN 
        alumno ON reporte_comentarios.alumno_id = alumno.id
    JOIN 
        grupo ON reporte_comentarios.grupo_id = grupo.id;
    ''')
    return cursor.fetchall()

#Asignar calificacion
def asignar_calificacion(cursor, alumno_id, calificacion):
    cursor.execute('''
    UPDATE alumno
    SET calificacion = ?
    WHERE id = ?''', (calificacion, alumno_id))

def obtener_alumno_con_calificacion(cursor, alumno_id):
    cursor.execute('''
    SELECT nombre, calificacion
    FROM alumno
    WHERE id = ?''', (alumno_id,))
    return cursor.fetchone()


def obtener_alumnos_por_grupo(cursor, grupo_id):
    cursor.execute('''
    SELECT alumno.id, alumno.nombre
    FROM alumno
    JOIN alumno_grupo ON alumno.id = alumno_grupo.alumno_id
    WHERE alumno_grupo.grupo_id = ?
    ''', (grupo_id,))
    return cursor.fetchall()

def obtener_datos_profesor(cursor, profesor_id, grupo_id):
    cursor.execute('''
    SELECT profesor.nombre, grupo.id, grupo.nombre
    FROM profesor
    JOIN profesor_grupo ON profesor.id = profesor_grupo.profesor_id
    JOIN grupo ON profesor_grupo.grupo_id = grupo.id
    WHERE profesor.id = ? AND grupo.id = ?
    ''', (profesor_id, grupo_id))
    return cursor.fetchall()

def obtener_profesor(cursor, profesor_id):
    cursor.execute('''
    SELECT nombre
    FROM profesor
    WHERE id = ?''', (profesor_id))
    return cursor.fetchone()

def obtener_supervisor(cursor, supervisor_id):
    cursor.execute('''
    SELECT nombre
    FROM supervisor
    WHERE id = ?''', (supervisor_id))
    return cursor.fetchone()

def obtener_director(cursor, director_id):
    cursor.execute('''
    SELECT nombre
    FROM director
    WHERE id = ?''', (director_id))
    return cursor.fetchone()



def asignar_calificaciones(cursor, profesor_id, grupo_id):
    # Obtener datos del profesor y el grupo específico
    datos_profesor = obtener_datos_profesor(cursor, profesor_id, grupo_id)
    for profesor_nombre, grupo_id, grupo_nombre in datos_profesor:
        print(f"Profesor: {profesor_nombre}, Grupo: {grupo_nombre}")
        # Obtener alumnos del grupo
        alumnos = obtener_alumnos_por_grupo(cursor, grupo_id)
        for alumno_id, alumno_nombre in alumnos:
            calificacion = random.randint(5,10)
            #while True:
             #   try:
              #      print(f"Ingrese la calificación para {alumno_nombre} es : {calificacion}")
               #     break
                #except ValueError:
                 #   print("Por favor, ingrese un número entero válido para la calificación.")
            
            asignar_calificacion(cursor, alumno_id, calificacion)
            print(f"Calificacion asignada a {alumno_nombre}: {calificacion}")


comentarios = [
    "Demuestra un gran entusiasmo por aprender y participar en clase.",
    "Su dedicación y esfuerzo se reflejan en sus excelentes resultados.",
    "Ha progresado notablemente en [área específica] gracias a su perseverancia.",
    "Es un compañero colaborativo y siempre dispuesto a ayudar a los demás.",
    "Su creatividad y pensamiento crítico enriquecen las discusiones en clase.",
    "Ha desarrollado habilidades de organización y gestión del tiempo muy efectivas.",
    "Se destaca por su capacidad de análisis y resolución de problemas.",
    "Es un estudiante autónomo y responsable con sus tareas y proyectos.",
    "Su participación activa en clase demuestra un gran interés por la materia.",
    "Ha superado las expectativas en [área específica] gracias a su dedicación.",
    "Con un poco más de esfuerzo y constancia, puede alcanzar todo su potencial.",
    "Necesita mejorar su organización y planificación para cumplir con los plazos.",
    "Debe prestar más atención en clase y participar activamente en las discusiones.",
    "Es importante que practique más [habilidad específica] para afianzar sus conocimientos.",
    "Sería beneficioso que buscara ayuda adicional si tiene dificultades en [área específica].",
    "Es fundamental que mejore su capacidad de concentración y atención en clase.",
    "Debe trabajar en su habilidad para trabajar en equipo y colaborar con sus compañeros.",
    "Es importante que se esfuerce por entregar sus tareas a tiempo y completas.",
    "Necesita mejorar su capacidad de análisis y comprensión de textos complejos.",
    "Debe desarrollar estrategias de estudio más efectivas para optimizar su aprendizaje."
]

def asignar_Comentarios(cursor, profesor_id, grupo_id):
    # Obtener datos del profesor y el grupo específico
    datos_profesor = obtener_datos_profesor(cursor, profesor_id, grupo_id)
    for profesor_nombre, grupo_id, grupo_nombre in datos_profesor:
        print(f"Profesor: {profesor_nombre}, Grupo: {grupo_nombre}")
        # Obtener alumnos del grupo
        alumnos = obtener_alumnos_por_grupo(cursor, grupo_id)
        for alumno_id, alumno_nombre in alumnos:
            comentario = random.choice(comentarios)
            #while True:
             #   try:
              #      comentario = input(f"Ingrese un comentario para {alumno_nombre}: ")
               #     break
                #except ValueError:
                 #   print("Error")
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Comentario de {alumno_nombre}: {comentario}" )
            escribir_reporte(cursor, profesor_id, alumno_id, grupo_id, comentario, fecha)

def obtener_grupos(cursor, profesor_id):
    # Ejecución de la consulta SQL para obtener los grupos del profesor por ID
    cursor.execute('''
        SELECT g.nombre, g.id
        FROM grupo g
        INNER JOIN profesor_grupo pg ON g.id = pg.grupo_id
        WHERE pg.profesor_id = ?
    ''', (profesor_id,))
    
    # Obtener el resultado de la consulta
    resultados = cursor.fetchall()
    
    # Comprobar si se encontraron grupos para el profesor
    if resultados:
        return [grupo for grupo in resultados]
    else:
        return []


def obtener_Reporte_Calificaciones(cursor, profesor_id, grupo_id):
    # Obtener datos del profesor y el grupo específico
    datos_profesor = obtener_datos_profesor(cursor, profesor_id, grupo_id)
    
    if not datos_profesor:
        return "No se encontraron datos para el profesor o el grupo especificado."
    
    profesor_nombre, grupo_id, grupo_nombre = datos_profesor[0]
    
    # Obtener alumnos del grupo y sus calificaciones
    alumnos = obtener_alumnos_por_grupo(cursor, grupo_id)
    
    # Construir el string con la información
    informacion = f"Profesor: {profesor_nombre}\nID del Curso: {grupo_id}\nNombre del Curso: {grupo_nombre}\n\nAlumnos y Calificaciones:\n"
    
    for alumno_id, alumno_nombre in alumnos:
        alumno = obtener_alumno_con_calificacion(cursor, alumno_id)
        if alumno:
            nombre_alumno, calificacion = alumno
            informacion += f"- {nombre_alumno}: {calificacion}\n"
        else:
            informacion += f"- {alumno_nombre}: Sin calificacion\n"
    
    return informacion

def vaciar_califiaciones(cursor, grupo_id, profesor_id):
    print()

def obtener_reporte_completo(cursor, profesor_id, grupo_id):
    # Obtener datos del profesor y el grupo específico
    cursor.execute('''
    SELECT profesor.nombre, grupo.id, grupo.nombre
    FROM profesor
    JOIN profesor_grupo ON profesor.id = profesor_grupo.profesor_id
    JOIN grupo ON profesor_grupo.grupo_id = grupo.id
    WHERE profesor.id = ? AND grupo.id = ?
    ''', (profesor_id, grupo_id))
    datos_profesor = cursor.fetchone()

    if not datos_profesor:
        return "No se encontraron datos para el profesor o el grupo especificado."
    
    profesor_nombre, grupo_id, grupo_nombre = datos_profesor
    
    # Obtener alumnos del grupo y sus comentarios
    cursor.execute('''
    SELECT alumno.nombre, comentarios.comentario
    FROM alumno
    JOIN alumno_grupo ON alumno.id = alumno_grupo.alumno_id
    JOIN comentarios ON alumno.id = comentarios.alumno_id
    WHERE alumno_grupo.grupo_id = ? AND comentarios.profesor_id = ?
    ''', (grupo_id, profesor_id))
    alumnos_comentarios = cursor.fetchall()
    
    # Construir el string con la información
    informacion = f"Profesor: {profesor_nombre}\nID del Curso: {grupo_id}\nNombre del Curso: {grupo_nombre}\n\nAlumnos y Comentarios:\n"
    
    for alumno_nombre, comentario in alumnos_comentarios:
        informacion += f"- {alumno_nombre}: {comentario}\n"
    
    # Añadir la fecha y hora del reporte
    fecha_reporte = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    informacion += f"\nReporte generado el: {fecha_reporte}\n"
    
    return informacion


#FUNCIONES PARA OBTENER LA LLAVE PUBLICA Y PRIVADA
def obtener_ClavesProfesor(cursor, profesor_id):
    cursor.execute('''
    SELECT clave_Privada,clave_Publica,iv
    FROM profesor
    WHERE id = ?''', (profesor_id))
    return cursor.fetchone()



#FUNCIONES PARA OBTENER LA LLAVE PUBLICA Y PRIVADA
def obtener_ClavesDirector(cursor, director_id):
    cursor.execute('''
    SELECT clave_Privada,clave_Publica,iv
    FROM director
    WHERE id = ?''', (director_id))
    return cursor.fetchone()



#FUNCIONES PARA OBTENER LA LLAVE PUBLICA Y PRIVADA
def obtener_ClavesSupervisor(cursor, supervisor_id):
    cursor.execute('''
    SELECT clave_Privada,clave_Publica,iv
    FROM supervisor
    WHERE id = ?''', (supervisor_id))
    return cursor.fetchone()

def actualizar_claves_profesor(cursor, profesor_id, clave_privada, clave_publica,iv):
    cursor.execute('''
    UPDATE profesor
    SET clave_Privada = ?, clave_Publica = ?, iv= ? WHERE id = ?''', (clave_privada, clave_publica, iv, profesor_id))
    # Asegúrate de confirmar los cambios si estás usando una conexión a una base de datos
    cursor.connection.commit()


def actualizar_claves_supervisor(cursor, profesor_id, clave_privada, clave_publica,iv):
    cursor.execute('''
    UPDATE supervisor
    SET clave_Privada = ?, clave_Publica = ?, iv= ? WHERE id = ?''', (clave_privada, clave_publica, iv, profesor_id))
    # Asegúrate de confirmar los cambios si estás usando una conexión a una base de datos
    cursor.connection.commit()

def actualizar_claves_director(cursor, profesor_id, clave_privada, clave_publica,iv):
    cursor.execute('''
    UPDATE director
    SET clave_Privada = ?, clave_Publica = ?, iv= ? WHERE id = ?''', (clave_privada, clave_publica, iv, profesor_id))
    # Asegúrate de confirmar los cambios si estás usando una conexión a una base de datos
    cursor.connection.commit()

