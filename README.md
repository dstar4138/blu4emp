blu4EMP 
========
 
blu4emp is a bluetooth interface for your EMP server. This is useful if you
have a device, like a phone that you want to use in your alert system, without
having to build a whole new Alarm or plug-in for it. It is intentionally using
a low version of python so that it can work in more places.

Uses
-----

blu4emp is two programs in one. An EMP interface, and a bluetooth server 
for devices that can't run python (i.e. a dumb-phone). Here's how it works:

Say you want to connect with a phone:

* Make sure your computer has bluetooth capabilities.
* Start up blu4emp in server mode on your computer.

        ./blu4emp.py -sr

* Make your device findable, and connect to your computer following the
  instructions on your device.

Now all you have to do is wait for an alert! Your device will show a 
message, or play a sound to indicate there was an alert via EMP!! How cool
is that! Remember EMP can use SMS anyway, so this might not be what you
want to use. 
    

Say you want to connect with a smart phone or handheld device capable of
running blu4emp in client mode.
      
* Make sure your computer has bluetooth capabilities
* Start up blu4emp in server mode on your computer.

         ./blu4emp.py -sr 8080

* Make your device findable, and connect to your computer following the
  instructions on your device.
* Start up blu4emp in client mode on your device, and follow 
  instructions:   

         ./blu4emp.py -co 1234 01:23:45:67:89:AB
    
Now you can run commands like you would with emp, and also get constant 
alerts!! yay!!

