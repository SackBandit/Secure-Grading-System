import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def generar_clave_aes():
    # Generar una clave AES de 32 bytes (256 bits)
    return get_random_bytes(32)

# Función para cifrar con AES
def cifrar_aes(texto_plano, clave):
    # Crear un nuevo objeto AES en modo CBC con una clave y un IV aleatorios
    cipher = AES.new(clave, AES.MODE_CBC)
    iv = cipher.iv
    
    # Asegurarse de que el texto plano esté en formato bytes
    if isinstance(texto_plano, str):
        texto_plano_bytes = texto_plano.encode('utf-8')
    else:
        texto_plano_bytes = texto_plano
    
    # Cifrar el texto plano con padding
    texto_cifrado = cipher.encrypt(pad(texto_plano_bytes, AES.block_size))
    
    return iv, texto_cifrado

# Función para descifrar con AES
def descifrar_aes(iv, texto_cifrado, clave):
    cipher = AES.new(clave, AES.MODE_CBC, iv=iv)
    texto_plano_bytes = unpad(cipher.decrypt(texto_cifrado), AES.block_size)
    return texto_plano_bytes

# Función para hashear la contraseña
def hash_contraseña(contraseña):
    hash_obj = SHA256.new()
    hash_obj.update(contraseña.encode('utf-8'))
    return hash_obj.digest()

# Generar las claves RSA (esto se usa como ejemplo)
def generar_claves():
    key = RSA.generate(2048)
    clave_privada = key.export_key()
    clave_publica = key.publickey().export_key()
    return clave_privada, clave_publica


