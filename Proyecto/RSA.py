import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

def GenerarLlaves():
    # Generar un par de claves RSA (2048 bits)
    key = RSA.generate(2048)
    # Exportar la clave privada en formato DER
    clave_privada_der = key.export_key()
    # Exportar la clave pública en formato DER
    clave_publica_der = key.publickey().export_key()
    return clave_privada_der, clave_publica_der

def hash(texto):
     # Crear un nuevo objeto de hash
    hash_obj = SHA256.new()
    # Actualizar el objeto de hash con el texto
    hash_obj.update(texto.encode('utf-8'))
    # Obtener el valor del hash
    hash_value = hash_obj.digest()
    return hash_value


# Función para cifrar un mensaje con la clave pública RSA
def encrypt_message(message, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    message_bytes = message.encode('utf-8')
    encrypted_message = cipher.encrypt(message_bytes)
    return base64.b64encode(encrypted_message).decode('utf-8')

def decrypt_message(encrypted_message, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_message_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
    decrypted_message = cipher.decrypt(encrypted_message_bytes)
    return decrypted_message.decode('utf-8')

