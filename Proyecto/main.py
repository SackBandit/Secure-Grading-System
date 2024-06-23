import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DB.sql import obtener_profesor,conectar_bd,crear_tablas,obtener_grupos,asignar_calificaciones
#Iniciar sesión
def Cargo(operador):
    if operador=='Director':
        return director()
    elif operador=='Director':
        return supervisor()
    elif operador=='Profesor':
        return profesor()
    else:
        return "Proceso Finalizado"
    
def supervisor():
    print("Hola Supervisor")


def director():
    print("Hola director")


#Funciones del profesor
def AccionesProfesor(conn,cursor,clave,operador):
    if operador=='Calificar':
        print( 'Tienes los siguientes grupos:')
        obtener_grupos(cursor,clave)
        grupos = obtener_grupos(cursor, clave)
        # Mostrar los grupos obtenidos
        if grupos:
            print(f"\n---Grupos asignados---")
            i=1
            for grupo in grupos:
                
                print(i, ". ",grupo)
                i=i+1
            grupoCalif=input("Ingresa el grupo que quieres evarluar: ")
            asignar_calificaciones(cursor,clave,grupoCalif)
            # Realizar la acción
            conn.commit()
            
            print("\nGrupo Evaludado!")
        else:
            print(f"No se encontraron grupos para el profesor {clave}")

       

    elif operador=='Realizar Reportes':
        print('Realizar Reportes')
    elif operador=='Enviar Reporte':
        print('Enviar Reporte a supervisor')
    else:
        return "Proceso Finalizado"
    
def profesor():
    conn, cursor = conectar_bd('escuela.db')
    # Crear tablas
    crear_tablas(cursor)
    indentificador= input("Ingresa tu clave de trabajador: ")
    profesor=obtener_profesor(cursor,indentificador)
    if(profesor):
        print("Bienvenido, ",profesor[0])
        while(True):
            claveProfesor=indentificador
            print("\n\n\n¿Qué acción quieres realizar? \n1.Calificar \n2.Realizar Reporte \n3.Enviar Reporte")
            opcion= input("Ingresa tu opción: ")
            AccionesProfesor(conn,cursor,claveProfesor,opcion)
            # Cerrar la conexión
    else:
        print("Error al iniciar sesión")
    conn.close()
    
    



#Main
print("-----Bienvenido Usuario, por favor identificáte (Profesor, Supervisor, Director)-----")
identificacion = input("Ingresa tu cargo: ")
Cargo(identificacion)