import sys
import os
from datetime import datetime
import random
# Asegurar que la carpeta padre esté en el PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DB.sql import conectar_bd, crear_tablas,insertar_alumno,insertar_director,insertar_grupo,insertar_profesor,insertar_supervisor,asignar_alumno_a_grupo,asignar_profesor_a_grupo,escribir_reporte,asignar_calificaciones


def guardar_informacion_en_archivo(ruta_archivo, informacion):
    # Asegurarse de que el directorio existe
    directorio = os.path.dirname(ruta_archivo)
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(informacion)

{'''
# Conectar a la base de datos
conn, cursor = conectar_bd('escuela.db')
# Crear tablas
crear_tablas(cursor)



alumnos = [
    ("María", "García"),
    ("Juan", "López"),
    ("Ana", "Martínez"),
    ("Pedro", "Rodríguez"),
    ("Sofía", "González"),
    ("Carlos", "Fernández"),
    ("Laura", "Sánchez"),
    ("Luis", "Pérez"),
    ("Isabel", "Gómez"),
    ("Javier", "Díaz"),
    ("Carmen", "Moreno"),
    ("Miguel", "Jiménez"),
    ("Rosa", "Ruiz"),
    ("Alejandro", "Álvarez"),
    ("Lucía", "Romero"),
    ("Pablo", "Navarro"),
    ("Elena", "Torres"),
    ("Daniel", "Domínguez"),
    ("Marta", "Gil"),
    ("Sergio", "Vázquez"),
    ("Pilar", "Blanco"),
    ("José", "Serrano"),
    ("Raquel", "Ramírez"),
    ("Antonio", "Suárez"),
    ("Cristina", "Molina"),
    ("Francisco", "Morales"),
    ("Irene", "Ortega"),
    ("Manuel", "Delgado"),
    ("Teresa", "Castro"),
    ("David", "Marín"),
    ("Andrea", "Rubio"),
    ("Enrique", "Sanz"),
    ("Beatriz", "Nuñez"),
    ("Jorge", "Iglesias"),
    ("Silvia", "Medina"),
    ("Rafael", "Flores"),
    ("Nuria", "Vicente"),
    ("Fernando", "Garrido"),
    ("Inés", "Santos"),
    ("Ramón", "Lozano"),
    ("Eva", "Cano"),
    ("Eduardo", "Guerrero"),
    ("Ángela", "Cruz"),
    ("Víctor", "Hernández"),
    ("Yolanda", "Herrera")
]

id_grupo = insertar_grupo(cursor, 'Criptografía')  
id_grupo2 = insertar_grupo(cursor, 'Avanzadas')  
id_grupo3 = insertar_grupo(cursor, 'Topics of Criptography')
id_grupo4 = insertar_grupo(cursor, 'Sistemas en Chip')  
id_grupo5 = insertar_grupo(cursor, 'Diseño de sistemas digitales')
id_grupo6 = insertar_grupo(cursor, 'Inteligencia artificial')  
id_grupo7 = insertar_grupo(cursor, 'Sistemas Operatios') 
id_grupo8 = insertar_grupo(cursor, 'Móviles')  
id_grupo9 = insertar_grupo(cursor, 'Administración de Redes') 
id_grupo10 = insertar_grupo(cursor, 'Analisis y Diseño de Sistemas')  
id_grupo11 = insertar_grupo(cursor, 'FEPI')
id_grupo12 = insertar_grupo(cursor, 'Ingenieria de Software')   

id_director = insertar_director(cursor, 'Linares Vallejo Erick')
id_supervisor = insertar_supervisor(cursor, 'Mosso García', id_director)

id_profesor1 = insertar_profesor(cursor, 'Sandra Díaz', id_supervisor)
id_profesor2 = insertar_profesor(cursor, 'Idalia Maldonado', id_supervisor)
id_profesor3 = insertar_profesor(cursor, 'Veronica Domínguez', id_supervisor)
id_profesor4 = insertar_profesor(cursor, 'Nidia', id_supervisor)
id_profesor5 = insertar_profesor(cursor, 'Sigfrido Cifuentes', id_supervisor)
id_profesor6 = insertar_profesor(cursor, 'Ismael Mexicano', id_supervisor)

asignar_profesor_a_grupo(cursor, id_profesor1, id_grupo)
asignar_profesor_a_grupo(cursor, id_profesor1, id_grupo2)
asignar_profesor_a_grupo(cursor, id_profesor2, id_grupo3)
asignar_profesor_a_grupo(cursor, id_profesor2, id_grupo4)
asignar_profesor_a_grupo(cursor, id_profesor3, id_grupo5)
asignar_profesor_a_grupo(cursor, id_profesor3, id_grupo6)
asignar_profesor_a_grupo(cursor, id_profesor4, id_grupo7)
asignar_profesor_a_grupo(cursor, id_profesor4, id_grupo8)
asignar_profesor_a_grupo(cursor, id_profesor5, id_grupo9)
asignar_profesor_a_grupo(cursor, id_profesor5, id_grupo10)
asignar_profesor_a_grupo(cursor, id_profesor6, id_grupo11)
asignar_profesor_a_grupo(cursor, id_profesor6, id_grupo12)





for x in range(0, 240):
    y = x%12 + 1
    app = random.randint(0, 44)
    x2 = random.randint(0, 44)
    id_alumno = insertar_alumno(cursor, f"{alumnos[x2][0]} {alumnos[app][1]}")
    asignar_alumno_a_grupo(cursor, id_alumno, y)


conn.commit()
conn.close()

 '''}

# Ejemplo de inserción de datos
#id_director = insertar_director(cursor, 'Linares Vallejo')
#id_supervisor = insertar_supervisor(cursor, 'Mosso García', id_director)
#id_profesor = insertar_profesor(cursor, 'Sandra Díaz', id_supervisor)
#id_alumno = insertar_alumno(cursor, 'Isaac')
#id_alumno2 = insertar_alumno(cursor, 'Dany')
#id_alumno3 = insertar_alumno(cursor, 'Guillermo')
#id_grupo = insertar_grupo(cursor, 'Criptografía')  
#id_grupo2 = insertar_grupo(cursor, 'Topics of Critography')  
#asignar_profesor_a_grupo(cursor, id_profesor, id_grupo)
#asignar_profesor_a_grupo(cursor, id_profesor, id_grupo2)
#asignar_alumno_a_grupo(cursor, id_alumno, id_grupo2)
#asignar_alumno_a_grupo(cursor, id_alumno2, id_grupo)
#asignar_alumno_a_grupo(cursor, id_alumno3, id_grupo2)



#profesor_id = 1
#alumno_id = 1
#grupo_id = 1
#comentario = "El alumno ha mostrado un gran desempeño en las últimas semanas."
#fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#escribir_reporte(cursor, profesor_id, alumno_id, grupo_id, comentario, fecha)


#profesor_id = 1
#asignar_calificaciones(cursor, profesor_id,1)
#conn.commit()
#conn.close()