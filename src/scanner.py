#!/usr/bin/python2.5
""" I do not claim this is original work, it has been modified by me
to be more useful in blu4emp. see the examples for pybluez:
  http://code.google.com/p/pybluez/source/browse/trunk/examples/
"""
import bluetooth 


def scanForAll():
    print "looking for nearby devices..." 
    nearby_devices = bluetooth.discover_devices(lookup_names = True, 
                                                flush_cache = True, 
                                                duration = 10)
     
    print "found %d devices" % len(nearby_devices) 
    
    for addr, name in nearby_devices: 
        print " %s - %s" % (addr, name)
        for services in bluetooth.find_service(address = addr): 
            print " Name: %s" % (services["name"]) 
            print " Description: %s" % (services["description"]) 
            print " Protocol: %s" % (services["protocol"]) 
            print " Provider: %s" % (services["provider"]) 
            print " Port: %s" % (services["port"]) 
            print " Service id: %s" % (services["service-id"]) 
            print "" 
        print "" 

def scanForDevices():
    print "looking for nearby devices..." 
    nearby_devices = bluetooth.discover_devices(lookup_names = True, 
                                                flush_cache = True, 
                                                duration = 10)
     
    print "found %d devices" % len(nearby_devices) 
    
    for addr, name in nearby_devices: 
        print " %s - %s" % (addr, name)

def scanForEmpOnly():
    services = bluetooth.find_service(name="emp")
    if len(services) == 0:
        print "Couldn't find a computer hosting an EMP server with blu4emp running!"
    else:
        print "Found %d devices running emp" % len(services)
        for host in services:
            for point in host:
                print point,",",
            print ""
            
            
if __name__ == "__main__":
    """ Call individual methods, or just run it and scan for everything!"""
    scanForAll()
    