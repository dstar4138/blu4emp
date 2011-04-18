"""This is the ported code from the EMP codebase which is under copyright:

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
from socket import socket, AF_INET, SOCK_STREAM
        
class DaemonClientSocket():
    """A simple socket for connecting to a DaemonServerSocket. There is nothing
    special here except that it regulates the encoding and decoding of the 
    sent/recv messages for you.
    """
    def __init__(self, port=8080, bufferSize=1024, encoding="utf-8"):
        """ This is the socket for the Client connection. Make sure the server
        socket has the same port number and encoding that the client has.
        """
        self.BUFFER_SIZE = bufferSize
        self.PORT_NUM = port
        self.ENCODING = encoding
        self.RECV_LIMIT = 5 #DO NOT CHANGE!!
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.settimeout(0.5)#intentionally very low. DO NOT CHANGE!!
        
    def __getattr__(self, name):    
        return getattr(self.socket, name)
        
    def connect(self):
        """Connects to a currently running daemon on the local system. Make sure
        the daemon is utilizing a DaemonServerSocket and is the same encoding that
        you are using.
        """
        self.socket.connect(("localhost",self.PORT_NUM))
        
    def send(self,msg):
        """Sends a string as a byte sequence to a DaemonServerSocekt at the 
        other end. This essentially acts as a socket.sendall(msg), but if the 
        message is larger than the buffer-size it will throw an error. 
        """
        msg = str(msg)
        if len(msg) > self.BUFFER_SIZE:
            raise Exception("Message given is larger than buffer size!")
        
        try:
            self.socket.sendall(msg.encode(self.ENCODING))
            
        except AttributeError:
            raise TypeError("Parameter given is not a string.")
        except: raise     
        
    def _recv(self):
        """Receives a string as a byte sequence from a DaemonServerSocket at
        the other end. This acts like a loop receiving everything in the network
        buffer before returning. To protect from buffer overflow it has a set
        max limit to the number of receives, but its high enough that it wont 
        matter for most projects.
        """
        msg = ''
        try:
            count = 0
            while count < self.RECV_LIMIT:
                data = self.socket.recv(self.BUFFER_SIZE)
                
                if not data: break
                msg += data
                count+=1
        except: pass        
        finally:
            return msg.decode(self.ENCODING)
        
    def recv(self, block=True,blockout=10):
        """"""
        if not block:
            return self._recv()
        else:
            count=0
            msg = ""
            while count<blockout:
                msg = self._recv()
                if not msg:
                    count+=1
                    continue
                else:break
            return msg
    
    def close(self):
        """Closes the current connection with the Daemon."""
        self.socket.close()
                