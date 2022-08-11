# Proyecto 1
# Maria Jose Morales 19145

from helpers import clr_scr, enter_to_continue, main_menu, secondary_menu
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
import threading

class ListClients(slixmpp.ClientXMPP):
    '''Show roster'''
    
    def __init__(self, jid, password, user=None, presence_msg=None):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Handle events
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.contacts = []
        self.user = user
        self.user_details = None
        self.presence_msg = presence_msg

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # Jabber Search

    async def start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()

        user_list = []
        
        try:
            #Check the roster
            self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        
        self.presences.wait(3)

        roster = self.client_roster.groups()

        for group in roster:
            for user in roster[group]:
                details = self.client_roster.presence(user)
                if self.user and self.user == user:
                    
                    user_details = {}
                    status = None
                    show = None
                    priority = None

                    for key, value in details.items():
                        if value['status']:
                            status = value['status']                                         #Get status
                        if value['show']:
                            show = value['show']                                             #Get show
                        if value['priority']:
                            priority = value['priority']                                     #Get priority
                    
                    user_details['status'] = status
                    user_details['show'] = show
                    user_details['priority'] = priority

                    self.user_details = user_details

                if "alumchat.xyz" in user:
                    user_list.append(user)
        
        self.contacts = user_list

        if self.presence_msg:
            for contact in self.contacts:
                self.sendPresenceMsg(contact)

        if self.user:
            print("\n" + self.user_details)
        else:
            if len(user_list) == 0:
                print('No tienes contactos.')

            for contact in user_list:
                print('User: ' + contact)

        self.disconnect()
    
    def sendPresenceMsg(self, jid):
        '''Send Msg'''

        message = self.Message()
        message['to'] = jid
        message['type'] = 'chat'
        message['body'] = self.presence_msg

        try:
            message.send()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')

class SubscribeClient(slixmpp.ClientXMPP):
    '''Add a new contact'''

    def __init__(self, jid, password, new_contact):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.new_contact = new_contact

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # Jabber Search


    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto=self.new_contact)
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
            
        self.disconnect()

class SendMsg(slixmpp.ClientXMPP):
    '''Send and receive msgs'''

    def __init__(self, jid, password, to, msg):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.to = to
        self.msg = msg

        #Handle events
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.msg)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # Jabber Search

    async def start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()

        #Send message of type chat
        self.send_message(mto=self.to,
                          mbody=self.msg,
                          mtype='chat')

        self.disconect()

    def message(self, msg):
        #Print message
        if msg['type'] in ('chat'):
            to = msg['to']
            body = msg['body']
            
            #print the message and the receiver
            print(str(to) +  ": " + str(body))

            #Ask new message
            new_msg = input(">>")

            #Send message
            self.send_message(mto=self.to,
                              mbody=new_msg)


class DeleteAccount(slixmpp.ClientXMPP):
    '''Delete an account'''

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        #Handle events
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()

        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            #Send the delete iq
            delete.send(now=True)

        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        except Exception as e:
            print(e)  

        self.disconnect()