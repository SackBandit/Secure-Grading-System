from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

def generar_clave_aes():
    """Genera una clave AES de 256 bits."""
    return get_random_bytes(32)

def cifrar_con_aes(texto_plano, clave_aes):
    """Cifra el texto plano utilizando AES en modo CBC."""
    iv = get_random_bytes(AES.block_size)
    cipher_aes = AES.new(clave_aes, AES.MODE_CBC, iv)
    padding = AES.block_size - len(texto_plano) % AES.block_size
    texto_plano += bytes([padding]) * padding
    texto_cifrado = iv + cipher_aes.encrypt(texto_plano)
    return texto_cifrado

def descifrar_con_aes(texto_cifrado, clave_aes):
    """Descifra el texto cifrado utilizando AES en modo CBC."""
    iv = texto_cifrado[:AES.block_size]
    cipher_aes = AES.new(clave_aes, AES.MODE_CBC, iv)
    texto_descifrado = cipher_aes.decrypt(texto_cifrado[AES.block_size:])
    padding = texto_descifrado[-1]
    texto_descifrado = texto_descifrado[:-padding]
    return texto_descifrado

def generar_par_claves_rsa():
    """Genera un par de claves RSA (2048 bits)."""
    return RSA.generate(2048)

def cifrar_con_rsa(texto_plano, clave_publica_rsa):
    """Cifra el texto plano utilizando RSA-OAEP con la clave pública RSA proporcionada."""
    cipher_rsa = PKCS1_OAEP.new(clave_publica_rsa)
    texto_cifrado = cipher_rsa.encrypt(texto_plano)
    return texto_cifrado

def descifrar_con_rsa(texto_cifrado, clave_privada_rsa):
    """Descifra el texto cifrado utilizando RSA-OAEP con la clave privada RSA proporcionada."""
    cipher_rsa = PKCS1_OAEP.new(clave_privada_rsa)
    texto_descifrado = cipher_rsa.decrypt(texto_cifrado)
    return texto_descifrado

# Ejemplo de uso
{'''
# Datos para el cifrado AES
reporte_original = """
Profesor: Sandra Díaz
ID del Curso: 1
Nombre del Curso: Criptografía

Alumnos y Calificaciones:
- Dany: 10
"""

# Generar clave AES y cifrar el reporte
clave_aes = generar_clave_aes()
reporte_cifrado_aes = cifrar_con_aes(reporte_original.encode('utf-8'), clave_aes)

# Generar par de claves RSA
par_claves_rsa = generar_par_claves_rsa()
clave_publica_rsa = par_claves_rsa.publickey()
clave_privada_rsa = par_claves_rsa

# Cifrar la clave AES con RSA usando la clave pública
clave_aes_cifrada = cifrar_con_rsa(clave_aes, clave_publica_rsa)

# Descifrar la clave AES cifrada con RSA usando la clave privada
clave_aes_descifrada = descifrar_con_rsa(clave_aes_cifrada, clave_privada_rsa)

# Descifrar el reporte utilizando la clave AES descifrada
reporte_descifrado = descifrar_con_aes(reporte_cifrado_aes, clave_aes_descifrada)

# Imprimir resultados
print("Clave AES generada:", clave_aes.hex())
print("\nClave AES cifrada con RSA (base64):")
print(base64.b64encode(clave_aes_cifrada).decode('utf-8'))
print("\nReporte cifrado con AES (hexadecimal):")
print(reporte_cifrado_aes.hex())
print("\nClave AES descifrada:", clave_aes_descifrada.hex())
print("\nReporte descifrado:")
print(reporte_descifrado.decode('utf-8'))  # Decodificar el reporte descifrado como UTF-8
'''}