import sys
import os
from datetime import datetime
import random
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
# Asegurar que la carpeta padre esté en el PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DB.sql import conectar_bd, crear_tablas,insertar_alumno,insertar_director,insertar_grupo,insertar_profesor,insertar_supervisor,asignar_alumno_a_grupo,asignar_profesor_a_grupo,escribir_reporte,asignar_calificaciones
from AES import generar_clave_aes,cifrar_aes,descifrar_aes
from RSA import encrypt_message,decrypt_message

def guardar_informacion_en_archivo(ruta_archivo, informacion):
    # Asegurarse de que el directorio existe
    directorio = os.path.dirname(ruta_archivo)
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(informacion)


def Profesor_SupervisorCypher(texto_plano, llavePublica):
    # Aquí asumimos que `texto_plano` es una cadena de texto (str)
    clave = generar_clave_aes()
    iv, texto_cifrado = cifrar_aes(texto_plano, clave)
    k = encrypt_message(clave, llavePublica)
    return iv, texto_cifrado, k
 
def Profesor_SupervisorDeCypher(clave_rsa, k):
    # Decodificar la clave privada RSA desde formato PEM
    clave_rsa_decodificada = RSA.import_key(clave_rsa)
    
    # Crear un objeto cipher RSA para descifrar
    cipher_rsa = PKCS1_OAEP.new(clave_rsa_decodificada)
    
    # Descifrar la clave de sesión K con RSA
    llaveK = cipher_rsa.decrypt(k)
    print(llaveK)
    ## Decodificar IV desde base64
    #iv = base64.b64decode(iv_Des)
    
    # Descifrar el mensaje con AES
    #cipher_aes = AES.new(llaveK, AES.MODE_CBC, iv)
    #texto_plano = cipher_aes.decrypt(msj_cifrado)
    
    # Eliminar el padding PKCS7
    #texto_plano = eliminar_padding_PKCS7(texto_plano)
    
    return 1 #texto_plano.decode('utf-8')

# Función auxiliar para eliminar el padding PKCS7
def eliminar_padding_PKCS7(data):
    pad = data[-1]
    return data[:-pad]
{'''
# Conectar a la base de datos
conn, cursor = conectar_bd('escuela.db')
# Crear tablas
crear_tablas(cursor)


alumnos = [
    ("Maria", "Garcia"),
    ("Juan", "Lopez"),
    ("Ana", "Martinez"),
    ("Pedro", "Rodriguez"),
    ("Sofia", "Gonzalez"),
    ("Carlos", "Fernandez"),
    ("Laura", "Sanchez"),
    ("Luis", "Perez"),
    ("Isabel", "Gomez"),
    ("Javier", "Diaz"),
    ("Carmen", "Moreno"),
    ("Miguel", "Jimenez"),
    ("Rosa", "Ruiz"),
    ("Alejandro", "Alvarez"),
    ("Lucia", "Romero"),
    ("Pablo", "Navarro"),
    ("Elena", "Torres"),
    ("Daniel", "Dominguez"),
    ("Marta", "Gil"),
    ("Sergio", "Vazquez"),
    ("Pilar", "Blanco"),
    ("Jose", "Serrano"),
    ("Raquel", "Ramirez"),
    ("Antonio", "Suarez"),
    ("Cristina", "Molina"),
    ("Francisco", "Morales"),
    ("Irene", "Ortega"),
    ("Manuel", "Delgado"),
    ("Teresa", "Castro"),
    ("David", "Marin"),
    ("Andrea", "Rubio"),
    ("Enrique", "Sanz"),
    ("Beatriz", "Nunez"),
    ("Jorge", "Iglesias"),
    ("Silvia", "Medina"),
    ("Rafael", "Flores"),
    ("Nuria", "Vicente"),
    ("Fernando", "Garrido"),
    ("Ines", "Santos"),
    ("Ramon", "Lozano"),
    ("Eva", "Cano"),
    ("Eduardo", "Guerrero"),
    ("Angela", "Cruz"),
    ("Victor", "Hernandez"),
    ("Yolanda", "Herrera")
]

id_grupo = insertar_grupo(cursor, 'Criptografia')  
id_grupo2 = insertar_grupo(cursor, 'Avanzadas')  
id_grupo3 = insertar_grupo(cursor, 'Topics of Criptography')
id_grupo4 = insertar_grupo(cursor, 'Sistemas en Chip')  
id_grupo5 = insertar_grupo(cursor, 'Diseno de sistemas digitales')
id_grupo6 = insertar_grupo(cursor, 'Inteligencia artificial')  
id_grupo7 = insertar_grupo(cursor, 'Sistemas Operatios') 
id_grupo8 = insertar_grupo(cursor, 'Moviles')  
id_grupo9 = insertar_grupo(cursor, 'Administracion de Redes') 
id_grupo10 = insertar_grupo(cursor, 'Analisis y Diseno de Sistemas')  
id_grupo11 = insertar_grupo(cursor, 'FEPI')
id_grupo12 = insertar_grupo(cursor, 'Ingenieria de Software')   

id_director = insertar_director(cursor, 'Linares Vallejo Erick')
id_supervisor = insertar_supervisor(cursor, 'Mosso García', id_director)

id_profesor1 = insertar_profesor(cursor, 'Sandra Diaz', id_supervisor)
id_profesor2 = insertar_profesor(cursor, 'Idalia Maldonado', id_supervisor)
id_profesor3 = insertar_profesor(cursor, 'Veronica Dominguez', id_supervisor)
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