import sys
import os

# Asegurar que la carpeta padre esté en el PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DB.sql import conectar_bd, crear_tablas,insertar_alumno,insertar_director,insertar_grupo,insertar_profesor,insertar_supervisor,asignar_alumno_a_grupo,asignar_profesor_a_grupo

# Conectar a la base de datos
conn, cursor = conectar_bd('escuela.db')
# Crear tablas
crear_tablas(cursor)

# Ejemplo de inserción de datos
#id_director = insertar_director(cursor, 'Linares Vallejo')
#id_supervisor = insertar_supervisor(cursor, 'Mosso', id_director)
#id_profesor = insertar_profesor(cursor, 'Sandra Díaz', id_supervisor)
#id_alumno = insertar_alumno(cursor, 'Ohtli')
#id_grupo = insertar_grupo(cursor, 'Criptografía')  
#asignar_profesor_a_grupo(cursor, id_profesor, id_grupo)
#asignar_alumno_a_grupo(cursor, id_alumno, 1)



conn.commit()
conn.close()