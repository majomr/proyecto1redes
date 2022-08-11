# Proyecto 1
# Maria Jose Morales 19145


from os import system, name
import getpass

def clr_scr():
    '''Clear Screen'''

    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def enter_to_continue():
    '''Press Enter to continue'''

    input("\nPresiona ENTER para continuar.")

def get_password():
    '''Get Password'''
    try:
        p = getpass.getpass()
    except Exception as error:
        print('ERROR', error)
    else:
        return p
    
    return None


def main_menu():
    '''Main Menu'''    
    return '''
    
    Proyecto chat xmpp 

1. Registro
2. Iniciar Sesion
3. Salir
    '''

def login_menu():
    '''Login Menu'''

    return '''
    
    Inicia Sesion

    '''

def secondary_menu():
    '''Users Menu'''

    return '''
    
    Bienvenido a xmpp Chat

1. Contactos
2. Agregar un usuario a tus contactos
3. Detalles de un usuario (no sirve) 
4. Chats Personales
5. Chats Grupales (no sirve) 
6. Mensaje de Presencia
7. Enviar archivo (no sirve)
8. Cerrar Sesion
00. Eliminar cuenta

    '''