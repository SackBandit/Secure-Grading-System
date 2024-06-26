from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15


def firmar_documento(documento, clave_privada):
    key = RSA.import_key(clave_privada)
    h = SHA256.new(documento)
    firma = pkcs1_15.new(key).sign(h)
    return firma

def verificar_firma(documento, firma, clave_publica):
    key = RSA.import_key(clave_publica)
    h = SHA256.new(documento)
    try:
        pkcs1_15.new(key).verify(h, firma)
        print("La firma es válida.")
    except (ValueError, TypeError):
        print("La firma no es válida.")


# Firmar el documento
#firma = firmar_documento(documento, clave_privada)
#print("Firma:", firma)

# Verificar la firma
#verificar_firma(documento, firma, clave_publica)