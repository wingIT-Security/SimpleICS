# SimpleICS

This is a (very) simple ICS Network

To get this to run:

1. Connect a motor to a Raspberry Pi
2. Install Python (and Scapy) on Raspberry Pi
3. Set "listening_ip" to the IP that the HMI will be running on
4. Install Django on a computer (not the Raspberry Pi)
5. Set the "IP" from hmi/SimpleICS/hmi/webgui/views.py to the Raspberry Pi's IP Address
