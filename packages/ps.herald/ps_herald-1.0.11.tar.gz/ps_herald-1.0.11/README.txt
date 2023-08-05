Introduction
============

The Herald  package (https://psherald.readthedocs.io/en/latest/ps.html) provides three tools usable to 
monitor the behaviour of distributed applications

Herald's functionality is based on the **Basic** class, defined in the ps.basic package.

The **Basic** class enhances/uses the standard python logging package - especially  the ability to log messages 
to a stream-socket.

This package adds mechanisms to:

                - put these messages into a central database (bridge)
                - route/bridge  these messages to additional destinations (bridge)
                - display in a web-server (herald)
                - take actions on special messages (neelix)
                - take actions on lost system heartbeat (neelix)




 

