import base64
import json
import sys
import os
from Crypto.PublicKey import RSA
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DB.sql import obtener_profesor,conectar_bd,crear_tablas,obtener_grupos,asignar_calificaciones,asignar_Comentarios,obtener_Reporte_Calificaciones,obtener_reporte_completo,obtener_ClavesProfesor,actualizar_claves_profesor,obtener_supervisor,obtener_director,obtener_ClavesSupervisor,obtener_ClavesDirector,actualizar_claves_director,actualizar_claves_supervisor
from funcionesBD import guardar_informacion_en_archivo
from RSA import GenerarLlaves,hash,decrypt_message
from AES import cifrar_aes, hash_contraseña,descifrar_aes
from firma import firmar_documento,verificar_firma
from funcionesBD import Profesor_SupervisorCypher,Profesor_SupervisorDeCypher
import AES
from preba import generar_clave_aes,cifrar_con_aes,descifrar_con_aes,descifrar_con_rsa,cifrar_con_rsa
#Iniciar sesión
def Cargo(operador):
    if operador=='Director':
        return director()
    elif operador=='Supervisor':
        return supervisor()
    elif operador=='Profesor':
        return profesor()
    else:
        return "Proceso Finalizado"
    
def AccionesDirector(conn,cursor,clave,operador):
    if(operador=='Firmar'):
        Opcion= input('¿Revisará los documentos del profesor o supervisor?')
        if(Opcion =='Supervisor'): 
        
                    print("Tienes los siguientes documentos a firmar") 
                    ruta_directorio = "Director/DocumentosCifrados/Supervisor"  # Ruta al directorio
                    reportes = []
                    try:
                        archivos = os.listdir(ruta_directorio)
                        i = 1
                        for archivo in archivos:
                            print(f"{i}. {archivo}")
                            reportes.append(archivo)
                            i = i + 1
                    except FileNotFoundError:
                        print(f"El directorio '{ruta_directorio}' no se encontró.")
                    except PermissionError:
                        print(f"No tienes permisos para acceder al directorio '{ruta_directorio}'.")
                    
                    opcion = input('Ingrese el archivo JSON que quiere descifrar: ')
                    # Leer el archivo JSON
                    with open(f'Director/DocumentosCifrados/Supervisor/{opcion}.json', 'r',encoding='utf-8') as archivo:
                        datos_json = json.load(archivo)

                    # Decodificar los datos base64 de vuelta a bytes
                    texto_aes_base64 = datos_json["reporte_AES"]
                    texto_rsa_base64 = datos_json["claveAES_RSA"]

                    texto_aes_cifrado = base64.b64decode(texto_aes_base64)
                    texto_rsa_cifrado = base64.b64decode(texto_rsa_base64)

                    
                    print('Para descifrar la llave K de AES Ocuparemos tu clave privada')
                    password =input('Ingresa la contraseña que usaste para cifrar tu cp: ')
                    ClavePrivada,ClavePublica,iv=obtener_ClavesDirector(cursor,clave)
                    ClavePrivadaRecu= descifrar_aes(iv,ClavePrivada,hash_contraseña(password))
                    print('\n\n')
                    print(f'Clave Privada Recuperada: {ClavePrivadaRecu}')




                    clave_privada_rsa = RSA.import_key(ClavePrivadaRecu)
                    # Descifrar la clave AES cifrada con RSA usando la clave privada
                    clave_aes_descifrada = descifrar_con_rsa(texto_rsa_cifrado, clave_privada_rsa)
                    reporte_descifrado = descifrar_con_aes(texto_aes_cifrado, clave_aes_descifrada)
                    print("\nReporte descifrado:")
                    print(reporte_descifrado.decode('utf-8'))




                    print('Comprobar FIRMAR')
                    Profesor= input('Ingrese del supervisor: ')
                    clave_publicaP=obtener_ClavesSupervisor(cursor,Profesor)
                    mensaje= input('Ingrese el mensaje original: ')
                    firma= input('Ingrese la firma del documento: ')
                    print('\n')
                    verificar_firma((mensaje.replace(" ", "").replace("\n", "")).encode('utf-8'),base64.b64decode(firma),clave_publicaP[1])
                    



                    print('Ahora podrás firmar el documento')
                    print('Ocuparemos tu clave privada')
                    password =input('Ingresa la contraseña que usaste para cifrar tu cp: ')
                    ClavePrivada,ClavePublica,iv=obtener_ClavesDirector(cursor,clave)
                    ClavePrivadaRecu= descifrar_aes(iv,ClavePrivada,hash_contraseña(password))
                    print('\n\n')
                    print(f'Clave Privada Recuperada: {ClavePrivadaRecu}')
                    firma = firmar_documento((reporte_descifrado.decode('utf-8').replace(" ", "").replace("\n", "")).encode('utf-8'),ClavePrivadaRecu)
                    print(f"Firma del supervisor: {base64.b64encode(firma).decode('utf-8')}")
                    print('\n\nREPORTE FIRMADO\n')
                    ContenidoEnviar = (reporte_descifrado.decode('utf-8') +'\n'+ 'Firma del Supervisor: '+ base64.b64encode(firma).decode('utf-8'))
                    print(ContenidoEnviar)
                    print('\n')


                    clave_aes = generar_clave_aes()
                    Priv, obtenerPublicaSuper,iv = obtener_ClavesDirector(cursor,'1')
                    reporte_cifrado_aes = cifrar_con_aes(ContenidoEnviar.encode('utf-8'), clave_aes)
                            
                    # Cargar la clave pública RSA desde los bytes
                    clave_publica_rsa = RSA.import_key(obtenerPublicaSuper)

                    clave_aes_cifrada = cifrar_con_rsa(clave_aes,clave_publica_rsa)

                    print('Reporte cifrado con AES: ',reporte_cifrado_aes)
                    print('\n')
                    print('Clave AES cifrada: ',clave_aes_cifrada)
                            # Convertir bytes cifrados a base64

                    texto_aes_base64 = base64.b64encode(reporte_cifrado_aes).decode('utf-8')
                    texto_rsa_base64 = base64.b64encode(clave_aes_cifrada).decode('utf-8')

                    # Crear un diccionario con los datos
                    datos_json = {
                                "reporte_AES": texto_aes_base64,
                                "claveAES_RSA": texto_rsa_base64
                            }
                    datos_cifrados= input('Nombre del archivo: ')
                    # Guardar el diccionario como JSON en un archivo
                    with open(f'Director/DocumentosCifrados/{datos_cifrados}.json', 'w') as archivo:
                            json.dump(datos_json, archivo)
                            print("Datos cifrados guardados en datos_cifrados.json")

                
        elif(Opcion=='Profesores'):
            print("Solo puedes Descifrar estos documentos") 
            ruta_directorio = "Director/DocumentosCifrados/Profesores"  # Ruta al directorio
            reportes = []
            try:
                archivos = os.listdir(ruta_directorio)
                i = 1
                for archivo in archivos:
                    print(f"{i}. {archivo}")
                    reportes.append(archivo)
                    i = i + 1
            except FileNotFoundError:
                print(f"El directorio '{ruta_directorio}' no se encontró.")
            except PermissionError:
                print(f"No tienes permisos para acceder al directorio '{ruta_directorio}'.")
            
            opcion = input('Ingrese el archivo JSON que quiere descifrar: ')
            # Leer el archivo JSON
            with open(f'Director/DocumentosCifrados/Profesores/{opcion}.json', 'r',encoding='utf-8') as archivo:
                datos_json = json.load(archivo)

            # Decodificar los datos base64 de vuelta a bytes
            texto_aes_base64 = datos_json["reporte_AES"]
            texto_rsa_base64 = datos_json["claveAES_RSA"]

            texto_aes_cifrado = base64.b64decode(texto_aes_base64)
            texto_rsa_cifrado = base64.b64decode(texto_rsa_base64)

           
            

            print('Para descifrar la llave K de AES Ocuparemos tu clave privada')
            password =input('Ingresa la contraseña que usaste para cifrar tu cp: ')
            ClavePrivada,ClavePublica,iv=obtener_ClavesDirector(cursor,clave)
            ClavePrivadaRecu= descifrar_aes(iv,ClavePrivada,hash_contraseña(password))
            print('\n\n')
            print(f'Clave Privada Recuperada: {ClavePrivadaRecu}')

            clave_privada_rsa = RSA.import_key(ClavePrivadaRecu)
            # Descifrar la clave AES cifrada con RSA usando la clave privada
            clave_aes_descifrada = descifrar_con_rsa(texto_rsa_cifrado, clave_privada_rsa)
            reporte_descifrado = descifrar_con_aes(texto_aes_cifrado, clave_aes_descifrada)
            print("\nReporte descifrado:")
            print(reporte_descifrado.decode('utf-8'))

            print('Comprobar FIRMAR')
            Profesor= input('Ingrese el ID del profesor: ')
            clave_publicaP=obtener_ClavesProfesor(cursor,Profesor)
            mensaje= input('Ingrese el mensaje original: ')
            firma= input('Ingrese la firma del documento: ')
            print('\n')
            verificar_firma((mensaje.replace(" ", "").replace("\n", "")).encode('utf-8'),base64.b64decode(firma),clave_publicaP[1])
            
            
    elif operador=='Generar Llaves':
        llaves=obtener_ClavesDirector(cursor,clave)
        if  llaves[0] is not None:
            print("Ya posees la llave pública y privada, consulta con gestión para obtener unas nuevas!")
        else:
            
            print("No posees la llave publica y privada, te generaremos las llaves a continuación: ")
            llavePrivada, llavePublica= GenerarLlaves()
            print('Llave pública: ', llavePublica.decode('utf-8'))
            print('\n\nLlave privada: ', llavePrivada.decode('utf-8'))
            print('\n')
          
            print("\n\nCifraremos la llave privada con AES para mayor seguridad")
            password = input('Ingresar una contraseña para cifrar (NUNCA OLVIDES ESTA CONTRASEÑA): ')
            passwordHash = hash_contraseña(password)
            print("\nContraseña con HASH: ",passwordHash) 
            iv,passwordAES = cifrar_aes(llavePrivada,passwordHash)
            print("\nContraseña con AES: ",base64.b64encode(passwordAES).decode('utf-8'))
            print('Para recuperar tu clave privada se te pedirá ingresar la contraseña que ingresaste aquí')
            #print("\n\nContraseña descifrada: ",descifradoAES(passwordAES,passwordHash))
            actualizar_claves_director(cursor,clave,passwordAES,llavePublica,iv)
            # Realizar la acción
            conn.commit()


def AccionesSupervisor(conn,cursor,clave,operador):

    if operador=='Firmar':
            print("Tienes los siguientes documentos a firmar") 
            ruta_directorio = "Supervisor/DocumentosCifrados"  # Ruta al directorio
            reportes = []
            try:
                archivos = os.listdir(ruta_directorio)
                i = 1
                for archivo in archivos:
                    print(f"{i}. {archivo}")
                    reportes.append(archivo)
                    i = i + 1
            except FileNotFoundError:
                print(f"El directorio '{ruta_directorio}' no se encontró.")
            except PermissionError:
                print(f"No tienes permisos para acceder al directorio '{ruta_directorio}'.")
            
            opcion = input('Ingrese el archivo JSON que quiere descifrar: ')
            # Leer el archivo JSON
            with open(f'Supervisor/DocumentosCifrados/{opcion}.json', 'r',encoding='utf-8') as archivo:
                datos_json = json.load(archivo)

            # Decodificar los datos base64 de vuelta a bytes
            texto_aes_base64 = datos_json["reporte_AES"]
            texto_rsa_base64 = datos_json["claveAES_RSA"]

            texto_aes_cifrado = base64.b64decode(texto_aes_base64)
            texto_rsa_cifrado = base64.b64decode(texto_rsa_base64)

            # Convertir a formato hexadecimal si es necesario
            #texto_aes_hexa = texto_aes_cifrado.hex()
            #texto_rsa_hexa = texto_rsa_cifrado.hex()

            #print("Texto AES cifrado en hexadecimal:")
            #print(texto_aes_hexa)

            #print("\nTexto RSA cifrado en hexadecimal:")
            #print(texto_rsa_hexa)

            print('Para descifrar la llave K de AES Ocuparemos tu clave privada')
            password =input('Ingresa la contraseña que usaste para cifrar tu cp: ')
            ClavePrivada,ClavePublica,iv=obtener_ClavesSupervisor(cursor,clave)
            ClavePrivadaRecu= descifrar_aes(iv,ClavePrivada,hash_contraseña(password))
            print('\n\n')
            print(f'Clave Privada Recuperada: {ClavePrivadaRecu}')

            clave_privada_rsa = RSA.import_key(ClavePrivadaRecu)
            # Descifrar la clave AES cifrada con RSA usando la clave privada
            clave_aes_descifrada = descifrar_con_rsa(texto_rsa_cifrado, clave_privada_rsa)
            reporte_descifrado = descifrar_con_aes(texto_aes_cifrado, clave_aes_descifrada)
            print("\nReporte descifrado:")
            print(reporte_descifrado.decode('utf-8'))

            print('Comprobar FIRMAR')
            Profesor= input('Ingrese el ID del profesor: ')
            clave_publicaP=obtener_ClavesProfesor(cursor,Profesor)
            mensaje= input('Ingrese el mensaje original: ')
            firma= input('Ingrese la firma del documento: ')
            print('\n')
            verificar_firma((mensaje.replace(" ", "").replace("\n", "")).encode('utf-8'),base64.b64decode(firma),clave_publicaP[1])
            
            print('Ahora podrás firmar el documento')
            print('Ocuparemos tu clave privada')
            password =input('Ingresa la contraseña que usaste para cifrar tu cp: ')
            ClavePrivada,ClavePublica,iv=obtener_ClavesSupervisor(cursor,clave)
            ClavePrivadaRecu= descifrar_aes(iv,ClavePrivada,hash_contraseña(password))
            print('\n\n')
            print(f'Clave Privada Recuperada: {ClavePrivadaRecu}')
            firma = firmar_documento((reporte_descifrado.decode('utf-8').replace(" ", "").replace("\n", "")).encode('utf-8'),ClavePrivadaRecu)
            print(f"Firma del supervisor: {base64.b64encode(firma).decode('utf-8')}")
            print('\n\nREPORTE FIRMADO\n')
            ContenidoEnviar = (reporte_descifrado.decode('utf-8') +'\n'+ 'Firma del Supervisor: '+ base64.b64encode(firma).decode('utf-8'))
            print(ContenidoEnviar)
            print('\n')
            clave_aes = generar_clave_aes()
            Priv, obtenerPublicaSuper,iv = obtener_ClavesDirector(cursor,'1')
            reporte_cifrado_aes = cifrar_con_aes(ContenidoEnviar.encode('utf-8'), clave_aes)
                    
            # Cargar la clave pública RSA desde los bytes
            clave_publica_rsa = RSA.import_key(obtenerPublicaSuper)

            clave_aes_cifrada = cifrar_con_rsa(clave_aes,clave_publica_rsa)

            print('Reporte cifrado con AES: ',reporte_cifrado_aes)
            print('\n')
            print('Clave AES cifrada: ',clave_aes_cifrada)
                    # Convertir bytes cifrados a base64

            texto_aes_base64 = base64.b64encode(reporte_cifrado_aes).decode('utf-8')
            texto_rsa_base64 = base64.b64encode(clave_aes_cifrada).decode('utf-8')

            # Crear un diccionario con los datos
            datos_json = {
                        "reporte_AES": texto_aes_base64,
                        "claveAES_RSA": texto_rsa_base64
                    }
            datos_cifrados= input('Nombre del archivo: ')
            # Guardar el diccionario como JSON en un archivo
            with open(f'Director/DocumentosCifrados/Supervisor/{datos_cifrados}.json', 'w') as archivo:
                    json.dump(datos_json, archivo)
                    print("Datos cifrados guardados en datos_cifrados.json")

    
    
    
    elif operador=='Realizar Reporte':
        print('Realizar Reportes')
        print( 'Tienes los siguientes grupos:')
        

    elif operador=='Enviar Reporte':
            print('Reportes')


    elif operador=='Generar Llaves':
        llaves=obtener_ClavesSupervisor(cursor,clave)
        if  llaves[0] is not None:
            print("Ya posees la llave pública y privada, consulta con gestión para obtener unas nuevas!")
        else:
            
            print("No posees la llave publica y privada, te generaremos las llaves a continuación: ")
            llavePrivada, llavePublica= GenerarLlaves()
            print('Llave pública: ', llavePublica.decode('utf-8'))
            print('\n\nLlave privada: ', llavePrivada.decode('utf-8'))
            print('\n')
          
            print("\n\nCifraremos la llave privada con AES para mayor seguridad")
            password = input('Ingresar una contraseña para cifrar (NUNCA OLVIDES ESTA CONTRASEÑA): ')
            passwordHash = hash_contraseña(password)
            print("\nContraseña con HASH: ",passwordHash) 
            iv,passwordAES = cifrar_aes(llavePrivada,passwordHash)
            print("\nContraseña con AES: ",base64.b64encode(passwordAES).decode('utf-8'))
            print('Para recuperar tu clave privada se te pedirá ingresar la contraseña que ingresaste aquí')
            #print("\n\nContraseña descifrada: ",descifradoAES(passwordAES,passwordHash))
            actualizar_claves_supervisor(cursor,clave,passwordAES,llavePublica,iv)
            # Realizar la acción
            conn.commit()
            

def supervisor():
    conn, cursor = conectar_bd('escuela.db')
    # Crear tablas
    crear_tablas(cursor)
    indentificador= input("Ingresa tu clave de trabajador: ")
    supervisor=obtener_supervisor(cursor,indentificador)
    if(supervisor):
        print("Bienvenido supervisor, ",supervisor[0])
        while(True):
            claveProfesor=indentificador
            print("\n\n\n¿Qué acción quieres realizar? \n1.Firmar \n2.Generar Llaves")
            opcion= input("Ingresa tu opción: ")
            AccionesSupervisor(conn,cursor,claveProfesor,opcion)
            # Cerrar la conexión
    else:
        print("Error al iniciar sesión")
    conn.close()
    


def director():
    conn, cursor = conectar_bd('escuela.db')
    # Crear tablas
    crear_tablas(cursor)
    indentificador= input("Ingresa tu clave de trabajador: ")
    director=obtener_director(cursor,indentificador)
    if(supervisor):
        print("Bienvenido director, ",director[0])
        while(True):
            claveProfesor=indentificador
            print("\n\n\n¿Qué acción quieres realizar? \n1.Firmar \n2.Generar Llaves")
            opcion= input("Ingresa tu opción: ")
            AccionesDirector(conn,cursor,claveProfesor,opcion)
            # Cerrar la conexión
    else:
        print("Error al iniciar sesión")
    conn.close()





















#Funciones del profesor
def AccionesProfesor(conn,cursor,clave,operador):

    if operador=='Calificar':
        print( 'Tienes los siguientes grupos:')
        obtener_grupos(cursor,clave)
        grupos= obtener_grupos(cursor, clave)
        # Mostrar los grupos obtenidos
        if grupos:
            print(f"\n---Grupos asignados---")
            i=0
            for grupo in grupos:
                
                print(grupo[1], ". ",grupo[0])
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
                
                print(grupo[1], ". ",grupo[0])
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
                
                print(grupo[1], ". ",grupo[0])
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
            
            ruta_directorio = f"Profesores/{clave}"  # Ruta al directorio
            reportes = []

            try:
                archivos = os.listdir(ruta_directorio)
                i = 1
                for archivo in archivos:
                    print(f"{i}. {archivo}")
                    reportes.append(archivo)
                    i = i + 1
            except FileNotFoundError:
                print(f"El directorio '{ruta_directorio}' no se encontró.")
            except PermissionError:
                print(f"No tienes permisos para acceder al directorio '{ruta_directorio}'.")
            opcion=int(input('¿Cuál reporte quieres enviar? '))-1
            
            if 0 <= opcion < len(archivos):
                ruta_archivo = os.path.join(ruta_directorio, archivos[opcion])
                with open(ruta_archivo, "r") as f:
                    contenido = f.read()
                    print("\nContenido del archivo: ")
                    print(contenido)


                    #FIRMAR
                    print('Primeramente firmaremos el documento')
                    print('Ocuparemos tu clave privada')
                    password =input('Ingresa la contraseña que usaste para cifrar tu cp: ')
                    ClavePrivada,ClavePublica,iv=obtener_ClavesProfesor(cursor,clave)
                    ClavePrivadaRecu= descifrar_aes(iv,ClavePrivada,hash_contraseña(password))
                    print('\n\n')
                    print(f'Clave Privada Recuperada: {ClavePrivadaRecu}')
                    
                    
                    
                    firma = firmar_documento((contenido.replace(" ", "").replace("\n", "")).encode('utf-8'),ClavePrivadaRecu)
                    print(f"Firma del profesor: {base64.b64encode(firma).decode('utf-8')}")
                    print('\n\nREPORTE FIRMADO\n')
                    ContenidoEnviar = (contenido +'\n'+ 'Firma del profesor: '+ base64.b64encode(firma).decode('utf-8'))
                    print(ContenidoEnviar)
                    print('\n')
                    clave_aes = generar_clave_aes()
                    Priv, obtenerPublicaSuper,iv = obtener_ClavesSupervisor(cursor,'1')
                    reporte_cifrado_aes = cifrar_con_aes(ContenidoEnviar.encode('utf-8'), clave_aes)
                    
                    # Cargar la clave pública RSA desde los bytes
                    clave_publica_rsa = RSA.import_key(obtenerPublicaSuper)

                    clave_aes_cifrada = cifrar_con_rsa(clave_aes,clave_publica_rsa)

                    print('Reporte cifrado con AES: ',reporte_cifrado_aes)
                    print('\n')
                    print('Clave AES cifrada: ',clave_aes_cifrada)
                    # Convertir bytes cifrados a base64

                    texto_aes_base64 = base64.b64encode(reporte_cifrado_aes).decode('utf-8')
                    texto_rsa_base64 = base64.b64encode(clave_aes_cifrada).decode('utf-8')

                    # Crear un diccionario con los datos
                    datos_json = {
                        "reporte_AES": texto_aes_base64,
                        "claveAES_RSA": texto_rsa_base64
                    }
                    datos_cifrados= input('Nombre del archivo: ')
                    # Guardar el diccionario como JSON en un archivo
                    with open(f'Supervisor/DocumentosCifrados/{datos_cifrados}.json', 'w') as archivo:
                        json.dump(datos_json, archivo)
                    print("Datos cifrados guardados en datos_cifrados.json")
                   

                    #ENVIAR AL DIRECTOR
                    clave_aes = generar_clave_aes()
                    Priv, obtenerPublicaSuper,iv = obtener_ClavesDirector(cursor,'1')
                    reporte_cifrado_aes = cifrar_con_aes(ContenidoEnviar.encode('utf-8'), clave_aes)
                    
                    # Cargar la clave pública RSA desde los bytes
                    clave_publica_rsa = RSA.import_key(obtenerPublicaSuper)

                    clave_aes_cifrada = cifrar_con_rsa(clave_aes,clave_publica_rsa)

                    print('Reporte cifrado con AES: ',reporte_cifrado_aes)
                    print('\n')
                    print('Clave AES cifrada: ',clave_aes_cifrada)
                    # Convertir bytes cifrados a base64

                    texto_aes_base64 = base64.b64encode(reporte_cifrado_aes).decode('utf-8')
                    texto_rsa_base64 = base64.b64encode(clave_aes_cifrada).decode('utf-8')

                    # Crear un diccionario con los datos
                    datos_json = {
                        "reporte_AES": texto_aes_base64,
                        "claveAES_RSA": texto_rsa_base64
                    }
                    datos_cifrados= input('Nombre del archivo: ')
                    # Guardar el diccionario como JSON en un archivo
                    with open(f'Director/DocumentosCifrados/Profesores/{datos_cifrados}.json', 'w') as archivo:
                        json.dump(datos_json, archivo)
                    print("Datos cifrados guardados en datos_cifrados.json")
                   
                   
            
          
          


    elif operador=='Generar Llaves':
        llaves=obtener_ClavesProfesor(cursor,clave)
        if  llaves[0] is not None:
            print("Ya posees la llave pública y privada, consulta con gestión para obtener unas nuevas!")
        else:
            
            print("No posees la llave publica y privada, te generaremos las llaves a continuación: ")
            llavePrivada, llavePublica= GenerarLlaves()
            print('Llave pública: ', llavePublica.decode('utf-8'))
            print('\n\nLlave privada: ', llavePrivada.decode('utf-8'))
            print('\n')
          
            print("\n\nCifraremos la llave privada con AES para mayor seguridad")
            password = input('Ingresar una contraseña para cifrar (NUNCA OLVIDES ESTA CONTRASEÑA): ')
            passwordHash = hash_contraseña(password)
            print("\nContraseña con HASH: ",passwordHash) 
            iv,passwordAES = cifrar_aes(llavePrivada,passwordHash)
            print("\nContraseña con AES: ",base64.b64encode(passwordAES).decode('utf-8'))
            print('Para recuperar tu clave privada se te pedirá ingresar la contraseña que ingresaste aquí')
            #print("\n\nContraseña descifrada: ",descifradoAES(passwordAES,passwordHash))
            actualizar_claves_profesor(cursor,clave,passwordAES,llavePublica,iv)
            # Realizar la acción
            conn.commit()
            



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
            print("\n\n\n¿Qué acción quieres realizar? \n1.Calificar \n2.Realizar Comentarios \n3.Realizar Reporte \n4.Enviar Reporte \n5.Generar Llaves")
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