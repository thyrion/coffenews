Usefull Webpages:

Bluetooth Fix
http://raspberrypi.stackexchange.com/questions/41776/failed-to-connect-to-sdp-server-on-ffffff000000-no-such-file-or-directory

Bluetoothctl How-To
https://kofler.info/bluetooth-konfiguration-im-terminal-mit-bluetoothctl/

------------------

Python server:
https://github.com/karulis/pybluez/blob/master/examples/simple/rfcomm-server.py

Perlserver:
Dont remember anymore

perlserver.pl and server.py do basically the same.
The wait for a connection, ask the defined url for data and send the result to the Bluetooth Connection.
This connection ist closed afer data-transfer.


You can use BlueTerm2 (AndroidApp) for Testing.
Pair your mobile with the computer where you run the server.
Use bluetoothctl for discovery etc.

discoverable on
pairable on
(See Bluetoothctl HowTo)

Start one of the servers
Open the App, Longpress on the displayand select the Computer you justed paired for a connection.
you should see the dump of an xbm on the screen of your Android Device.

Remember:
This is all Bluetooth and NOT BLE !!!!!!
