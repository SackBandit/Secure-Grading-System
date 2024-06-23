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

    
def profesor():
    print("Hola profesor")


#Main
print("-----Bienvenido Usuario, por favor identificáte (Profesor, Supervisor, Director)-----")
identificacion = input("Ingresa tu cargo: ")
Cargo(identificacion)