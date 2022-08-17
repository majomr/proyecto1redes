# Proyecto 1
# Maria Jose Morales 19145

from client import DeleteAccount, ListClients, MUC, SendFile, SendMsg, SubscribeClient
from registration import Register
from helpers import clr_scr, enter_to_continue, get_password, main_menu, login_menu, secondary_menu


if __name__ == '__main__':
    
    wantsToContinue = True

    while wantsToContinue:
        
        #Clear Screen
        clr_scr()

        # Print Main Menu
        print(main_menu())

        main_menu_op = input("Ingrese una opcion: ")

        if main_menu_op == '1':
            '''Register'''
            
            clr_scr()
            
            print("\n\t\tRegistrar")

            jid = input("\nIngresa tu nombre de usuario: ")
            password = None
            while password == None:
                password = get_password()

            
            # Setup the RegisterBot and register plugins. Note that while plugins may
            # have interdependencies, the order in which you register them does
            # not matter.
            xmpp = Register(jid, password)

            # Some servers don't advertise support for inband registration, even
            # though they allow it. If this applies to your server, use:
            xmpp['xep_0077'].force_registration = True

            # Connect to the XMPP server and start processing XMPP stanzas.
            xmpp.connect()
            xmpp.process(forever=False)
            
            xmpp.disconnect()

            enter_to_continue()


        elif main_menu_op == '2':
            '''Iniciar Sesion'''
            
            #Clear Screen
            clr_scr()

            print(login_menu())

            jid = input("Ingresa tu nombre de usuario: ")
            password = None
            while password == None:
                password = get_password()

            wantsToContinue_2 = True
            while wantsToContinue_2:

                # Clear Screen
                clr_scr()

                # Print Menu
                print(secondary_menu())

                secondary_menu_op = input("Ingresa una opcion: ")

                if secondary_menu_op == '1':
                    '''Print Roster'''

                    clr_scr()

                    print("\n\t\tListado de contactos\n")

                    xmpp = ListClients(jid, password)
                    
                    xmpp.connect()
                    xmpp.process(forever=False)

                    enter_to_continue()
                
                elif secondary_menu_op == '2':
                    '''Add a contact'''

                    clr_scr()

                    print("\n\t\tAgregar un usuario a tus contactos\n")

                    new_contact = input("Ingresa tu nuevo contacto: ")

                    xmpp = SubscribeClient(jid, password, new_contact)
                    
                    xmpp.connect()
                    xmpp.process(forever=False)

                    enter_to_continue()
                
                elif secondary_menu_op == '3':
                    '''Show Specific user info'''

                    clr_scr()

                    print("\n\t\tMostrar detalles de un usuario\n")

                    see_contact = input("Ingresa nombre de contacto: ")

                    xmpp = ListClients(jid, password, see_contact)
            
                    xmpp.connect()
                    xmpp.process(forever=False)

                    enter_to_continue()
                    
                elif secondary_menu_op == '4':
                    '''Chats Personales'''

                    clr_scr()

                    print("\n\t\tChats Personales\n")

                    text_contact = input("Ingresa nombre de contacto: ")

                    msg = input(">>")

                    xmpp = SendMsg(jid, password, text_contact, msg)
                
                    xmpp.connect()
                    xmpp.process(forever=False)

                elif secondary_menu_op == '5':
                    '''Group Chats'''

                    clr_scr()

                    print("\n\t\tChats Grupales\n")

                    rjid = input("Ingresa Room JID: ")

                    alias = input("Ingresa tu alias: ")

                    xmpp = MUC(jid, password, rjid, alias)

                    xmpp.connect()
                    xmpp.process(forever=False)

                elif secondary_menu_op == '6':
                    '''Definir un mensaje de presencia'''

                    clr_scr()

                    print("\n\t\tDefinir Mensaje de Presencia\n")

                    presence_msg = input("Mensaje de presencia: ")

                    xmpp = ListClients(jid, password, presence_msg=presence_msg)

                    xmpp.connect()
                    xmpp.process(forever=False)
                
                elif secondary_menu_op == '7':
                    '''Send a file'''

                    clr_scr()

                    print("\n\t\tEnviar un archivo\n")

                    text_contact = input("Ingresa nombre de contacto: ")
                    path = input("Ingresa path del archivo: ")

                    xmpp = SendFile(jid, password, text_contact, path)

                    # Connect to the XMPP server and start processing XMPP stanzas.
                    xmpp.connect()
                    xmpp.process(forever=False)

                    enter_to_continue()

                elif secondary_menu_op == '8':
                    '''Close session'''

                    wantsToContinue_2 = False

                    jid = None
                    password = None

                elif secondary_menu_op == '00':
                    '''Delete Act'''

                    xmpp = DeleteAccount(jid, password)

                    wantsToContinue_2 = False

                    jid = None
                    password = None
                
                else:
                    print("\nOpcion ingresada no es valida.")
                    enter_to_continue()

        elif main_menu_op == '3':
            '''Exit'''
            wantsToContinue = False

        else:
            print("\nOpcion ingresada no es valida.")
            enter_to_continue()