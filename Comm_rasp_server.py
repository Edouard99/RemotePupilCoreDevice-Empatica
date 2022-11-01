import socket               # Import socket module
import sys
import time
import _thread
PORT=12345
try :
    PORT=int(sys.argv[1])
except Exception:
    None


s = socket.socket()         # Create a socket object
s.bind(('0.0.0.0', PORT))        # Bind to the port
s.settimeout(25)
s.listen(5)                 # Now wait for client connection.
t_start=time.time()
while True:
   try:
      c, addr = s.accept()     # Establish connection with client.
      msg=c.recv(1024)
      if True:
         print (msg.decode())
         c.close()
         break
   except socket.timeout:
      print(555)
      break
      