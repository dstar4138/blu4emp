#!/usr/bin/env python2.5
__copyright__="""
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

__large_desc__="""
    blu4emp is a bluetooth interface for your EMP server. This is useful if you
have a device, like a phone that you want to use in your alert system, without
having to build a whole new Alarm or plug-in for it. It is intentionally using
a low version of python so that it can work in more places.

    blu4emp is two programs in one. An EMP interface, and a bluetooth server 
for devices that can't run python (eg. a dumb-phone). Heres how it works:

    Say you want to connect with a phone:
        - Make sure your computer has bluetooth capabilities.
        - Start up blu4emp in server mode on your computer.
                        ./blu4emp.py -sr
        - Make your device findable, and connect to your computer following the
        instructions on your device.
    Now all you have to do is wait for an alert! Your device will show a 
    message, or play a sound to indicate there was an alert via EMP!! How cool
    is that! Remember EMP can use SMS anyway, so this might not be what you
    want... 
    
    Say you want to connect with a smart phone or handheld device capable of
      running blu4emp in client mode.
      
        - Make sure your computer has bluetooth capabilities
        - Start up blu4emp in server mode on your computer.
                        ./blu4emp.py -sr 8080
        - Make your device findable, and connect to your computer following the
        instructions on your device.
        - Start up blu4emp in client mode on your device, and follow 
        instructions:   ./blu4emp.py -co 1234 01:23:45:67:89:AB
    Now you can run commands like you would with emp, and also get constant 
    alerts!! yay!!
"""
import random
from optparse import OptionParser
__version__ = "0.1"
__usage__ = "%prog [ -c [ name | mac ] | -s [-r | -o code ] [ -n num ] dport ]"
__description__ = "blu4emp is an bluetooth interface for your EMP daemon."

## The default number of connections allowed.
__NUM_CONNECTIONS_DEFAULT = 1
## The max number of connections the server will allow at one time.
__NUM_CONNECTIONS_MAX = 10
## Max size of a connection code.
__CONN_CODE_MAXSIZE = 5  #!!! Can't be bigger than 10 !!!#


## User defined actual state.
__NUM_CONNECTIONS = 1
__CONN_CODE = ""
__KILL_WHEN_CONNECTED = True
__EMP_PORT = 8080


def setConnections(num):
    """ If running as the server. This is the number of connections to bi4emp 
    clients we will allow. DEFAULT=1
    """
    global __NUM_CONNECTIONS
    if type(num) == int:
        if num > 1 and num <= __NUM_CONNECTIONS_MAX:
            __NUM_CONNECTIONS = num
        else:
            raise Exception("Number of connections %d is invalid." % int(num))
            
def setCode(code):
    """ Set the code for connecting to a blu4emp server."""
    global __CONN_CODE
    if type(code) is str and len(code) <= __CONN_CODE_MAXSIZE:
        __CONN_CODE = code
    else:
        raise Exception("Code given is invalid.")
   
def main():
    """ Start everything up and run blu4emp! """
    global __CONN_CODE, __EMP_PORT,__NUM_CONNECTIONS,__KILL_WHEN_CONNECTED
    
    parser  = OptionParser(usage=__usage__, 
                           version="Version: blu4emp v"+__version__,
                           description=__description__ )

    parser.add_option("-c","--client", action="store_false", dest="state", help="Run in client mode.", default=False)
    parser.add_option("-s","--server", action="store_true",  dest="state", help="Run in server mode.")
    
    parser.add_option("-r",action="store_true",  dest="code", help="Randomize connection code.", default=False)
    parser.add_option("-o","--code", type="string", nargs=1, dest="ucode", help="Set default connection code.")

    parser.add_option("-n","--conns",type="int", dest="connections", nargs=1, help="Number of concurrent bluetooth connections allowed.")

    (options, args) = parser.parse_args()
    
    if len(args) > 1:
        parser.print_usage()
        return
        
    # set variables given!
    setConnections(options.connections)
        
    if options.code:
        # Random MAX digit code of just numbers 0-9.
        setCode("%s" % str(random.random())[2:2+__CONN_CODE_MAXSIZE])
    else:
        # User defined code!
        if options.ucode is None:
            parser.print_usage()
            return
        else:
            setCode(options.ucode)
    
    
    # Determine what we do!
    try:
        if options.state:
            if len(args)>0:__EMP_PORT = int(args[0])
            from blu4emp_server import serverMode
            serverMode(__CONN_CODE,
                       __EMP_PORT,
                       __NUM_CONNECTIONS,
                       __KILL_WHEN_CONNECTED)
        else: 
            macname = args[0]
            from blu4emp_client import clientMode
            clientMode(__CONN_CODE, macname )
            
    except Exception, e:
        print e
        
if __name__ == "__main__": main();
