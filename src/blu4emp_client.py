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
#   - Move client commands stuff to server
#   - make alert-mode default mode.


import sys
import bluetooth

#MAX NUMBER OF TIMES WE WILL TRY TO FIND THE EMP SERVICE
MAXCOUNT = 2
# What the user sees when they can input a command
PROMPT = "> "
# Commands that close the system
CLOSE = []    
# All the commands mapped to their function
COMMANDS = {}

## CAN USE IF YOU DONT CARE WHICH HOST TO CONNECT TO. ##
HOST_ANY = "*"


def cmd_error( *args ): 
    print "Command does not exist."
def cmd_help( *args ):
    print "Command list: "
    for cmd in COMMANDS:
        print " -",cmd
        
#TODO: Write some commands!!!        
def cmd_status( *args ):pass
def cmd_send( *args ):pass
def cmd_alarm_mode( *args ):pass


def boarder():
    for _ in range(1,80): print "-",
    print ""


def discoverEmpHosts():
    count = 0
    services = []
    while len(services) < 1 or count > MAXCOUNT:
        services = bluetooth.find_service(name="emp")
        
    if len(services) == 0:
        print "Couldn't find a computer hosting an EMP server with bi4emp running!"
        sys.exit(0)
    else:
        return services

def runUserCommands(conn):
    close = False
    setupCmds()
    print "Welcome, type 'help' for a list of commands."
    boarder()
    
    while not close:
        #####################################
        #          COMMAND LOOP             #
        #####################################
        cmd = raw_input( PROMPT )
        if cmd.lower() in CLOSE: 
            close = True
        else: 
            cmd = cmd.split(" ")
            COMMANDS.get(cmd[0].lower() ,cmd_error)(cmd[1:])
        print ""

    #returning will close the connection and print a nice msg
    return

def setupCmds():
    global COMMANDS, CLOSE
    CLOSE = ["exit","close","end","break"]
    COMMANDS = { "help":cmd_help,
                 "status":cmd_status,
                 "send":cmd_send,
                 "alarmmode":cmd_alarm_mode}

def clientMode(code, macname):
    """
    Connect to a bluetooth server on a host machine.
    """
    print "Looking for a host..."
    hosts = discoverEmpHosts()
    foundHost = None
    
    for host in hosts:
        if macname == HOST_ANY or \
           host["name"] == macname or \
           host["host"] == macname:
            foundHost = host
            break
        
    if foundHost is None:
        print "Could not find a host that matched the address or name you gave."
        print "Here is a list of the hosts that are running EMP: "
        for host in hosts:
            print "  -", host["name"],":",host["host"]
        boarder()
        sys.exit(0)
        
    # set up the bluetooth socket with the host    
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect(( foundHost["host"], foundHost["port"] ))
    print "Connecting with connection code:", code
    sock.send(code)
    
    # If the connection failed... 
    if sock.recv() == "proceed":
        print "Connected!!"
        boarder()
        runUserCommands(sock)
    
    print "Closing Connection..."
    sock.close()
    print "Connection closed"
    boarder() ; boarder()


if __name__ == "__main__":
    """ Connects to the first host it finds with blu4emp running, and trys 
    connecting with the default password. If this is not what you want to do,
    then I suggest using the bi4emp.py interface for all your bluetoothy 
    goodness.
    """
    clientMode("1234", HOST_ANY)

