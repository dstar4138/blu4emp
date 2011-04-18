"""
Copyright (c) 2010-2011 Alexander Dean (dstar@csh.rit.edu)
Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and 
limitations under the License. 
"""

# TODO: 
#  - Add capability to utilize connected devices as alarms.
#     (eg. my dumb-phone vibrates/plays sound every time i get email)
#  - Move command parsing to server, client should be SMALL

import re
import bluetooth

from time      import sleep
from threading import Thread
from leftovers import DaemonClientSocket

_CONNECTIONS_ = 0
_INTERFACE_ID_ = ""

class BTSocket(): 
    """Want to wrap the bluetooth socket??"""
    pass


class BIHandler():
    """ These handle connections that have already connected."""
    def __init__(self, empconn, socket):
        self.empconn = empconn
        self.socket = socket
        _CONNECTIONS_+=1
        self.die = False
        Thread(target=self.emphandler).start()
        Thread(target=self.sockethandler).start()

    def kill(self):
        """ Handles killing the BIHandler threads."""
        if not self.die:
            self.die = True
            _CONNECTIONS_-=1 #indicate there is one less connection.
        
    def emphandler(self):
        """ Passes messages from emp to the bluetooth socket."""
        while not self.die:
            msg = self.socket.recv()
            if not msg: break
            else:       self.empconn.send(msg)
        self.kill()
             
    def sockethandler(self):
        """ Passes messages from the bluetooth socket to emp."""
        while not self.die:
            msg = self.empconn.recv()
            if not msg: break
            else:       self.socket.send(msg)
        self.kill()
  
    
def setID( msg ):    
    """ Since JSON doesn't exist in 2.5, we do our own parsing! """
    global _INTERFACE_ID_
    
    tokens = re.split("[\",:{}]+", str(msg))
    count=0
    #print tokens
    for token in tokens:            
        if token == "dest" and count+1 < len(tokens):
            _INTERFACE_ID_ = tokens[count+1]
            break
        count+=1

    if _INTERFACE_ID_ == "":
        raise Exception("Could not determine personal ID!")
    else:
        print "My Interface ID: ", _INTERFACE_ID_
    

def setupDaemonConn( portnum ):
    conn = DaemonClientSocket(port=portnum)
    try:
        conn.connect()
        msg = conn.recv()
        setID(msg)
        return conn
    except:
        raise Exception("Error: Could not contact EMP.")


def serverMode(code, empport, maxconn=1, killwhenconnected=True):
    """
    1.) set up a connection with EMP
    2.) start bluetooth socket server
    3.) get connection, push to handler
        - incoming commands push to emp
        - outgoing from emp push to socket
    4.) quit when asked
    """
    empconn = setupDaemonConn(empport)
    
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    port = bluetooth.PORT_ANY
    server_sock.bind(("",port))
    server_sock.listen(1)
    
    bluetooth.advertise_service(server_sock, "emp",
                     service_classes=[bluetooth.SERIAL_PORT_CLASS],
                     profiles=[bluetooth.SERIAL_PORT_PROFILE])
    
    print "Server information:--------" 
    print "\tName:", server_sock.getsockname()[0]
    print "\tPort:", server_sock.getsockname()[1]
    print "\tConnection Code:", code
    print "---------------------------"
    
    while 1: # TODO: WHEN DO I CLOSE???
        if _CONNECTIONS_ < maxconn:
            try:
                client_sock, address = server_sock.accept()
                print "Accepted connection from ", address
                attemptedCode = client_sock.recv()
                if attemptedCode == code:
                    client_sock.send("proceed")
                    BIHandler( empconn, client_sock )
                    print "pushed to handler..."
                else:
                    print "their code didnt match ours! (",attemptedCode,"!=",code,")"
            except: #timeout!
                sleep(8)
        elif killwhenconnected: break 
        else: sleep(8)
        
    print "Server shutting down with %d persistent connections..."%_CONNECTIONS_
    server_sock.close()

        
if __name__ == "__main__":
    """ If you just want to run the server with default everything, you can.
    Otherwise, I suggest you used blu4emp.py for all you bluetoothy goodness.
    """
    serverMode("1234",8080)