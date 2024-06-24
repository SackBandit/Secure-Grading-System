from Crypto import Random
from Crypto.Cipher import AES

import hashlib
from base64 import b64encode, b64decode

#Tamaño de bloque: 16 bytes o 124 bits
#Tamaño de llave: 16 bytes o 124 bits
#Modo de operación: CBC - Cipher Block Chaining


def pad(m):
        padding = AES.block_size - len(m) % AES.block_size
        ascii_string = chr(padding)
        padding_str = padding * ascii_string
        texto_con_pad = m + padding_str
        return texto_con_pad

def __unpad(m):
        last_character = m[len(m) - 1:]
        return m[:-ord(last_character)]

def generarLlave():
      k = Random.get_random_bytes(16)
      kascii = b64encode(k).decode("utf-8")
      print(f"Llave: {kascii}")
      return k
      

def cifrarAES(m):
    m = pad(m)
    iv = Random.new().read(AES.block_size)
    key = generarLlave()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    c = cipher.encrypt(m.encode())
    cascii = b64encode(iv+c).decode("utf-8")
    print(f"C: {cascii}")
    return b64encode(iv+c).decode("utf-8"), key

def descifradoAES(c, key):
        c = b64decode(c)
        iv = c[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        m = cipher.decrypt(c[AES.block_size:]).decode("utf-8")
        return __unpad(m)


m = "Me gustaria que estes aqui"
cifrarAES(m)
print(f"AES.blocksize: {AES.block_size}")






