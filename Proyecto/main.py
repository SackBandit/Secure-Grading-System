import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DB.sql import obtener_profesor,conectar_bd,crear_tablas,obtener_grupos,asignar_calificaciones,asignar_Comentarios,obtener_Reporte_Calificaciones,obtener_reporte_completo
from funcionesBD import guardar_informacion_en_archivo
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

       

    elif operador=='Realizar Comentarios':
        print('Realizar Comentarios')
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
            grupoComentario=input("Ingresa el grupo que quieres realizar comentarios: ")
            asignar_Comentarios(cursor,clave,grupoComentario)
            # Realizar la acción
            conn.commit()
            
            print("\nFicha descriptiva Finalizada!")
        else:
            print(f"No se encontraron grupos para el profesor {clave}")


        
    elif operador=='Realizar Reporte':
        #Aquí se obtienen los datos de los reportes de calificaciones y de comentarios
        #Se crea un txt del reporte que se quiere realizar 
        #Se ingresa el nombre del txt (Example: Reporte_Calif_Criptografía_FP)
        #FP: Firmado por profesor
        print('Realizar Reportes')
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
            grupoReporte=input("Ingresa el grupo que quieres realizar su reporte de calificaciones: ")
            reporteCalif= obtener_Reporte_Calificaciones(cursor,clave,grupoReporte)
            reporteComent=obtener_reporte_completo(cursor,clave,grupoReporte)
            print(reporteCalif)
            print('\n\n')
            print(reporteComent)


             # Construir la ruta completa del archivo
            nombre_archivo= input("Ingresa el nombre del archivo para guardarlo: ")
            archivo1=nombre_archivo+'_Calificaciones.txt'
            archivo2=nombre_archivo+'_Comentarios.txt'
            ruta_base = './Profesores'
            ruta_completa1 = os.path.join(ruta_base, clave, archivo1)
            ruta_completa2 = os.path.join(ruta_base, clave, archivo2)
            guardar_informacion_en_archivo(ruta_completa1,reporteCalif)
            guardar_informacion_en_archivo(ruta_completa2,reporteComent)
    
            # Realizar la acción
            conn.commit()
            print('Reportes Creados con Éxito!')
        else:
            print(f"No se encontraron grupos para el profesor {clave}")
    elif operador=='Enviar Reporte':
            #El usuario debe visualizar los reportes que contiene la carpeta
            #El usuario selecciona el reporte a enviar
            opcion=input('¿Cuál reporte quieres enviar?')
            #Se lee el archivo
            #Se aplica AES y RSA

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
            print("\n\n\n¿Qué acción quieres realizar? \n1.Calificar \n2.Realizar Comentarios \n3.Realizar Reporte \n4.Enviar Reporte")
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