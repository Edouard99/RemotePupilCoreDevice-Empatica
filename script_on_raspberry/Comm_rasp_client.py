import socket               # Import socket module
import sys
msg=55
IP="0.0.0.0" #'192.168.0.119'
PORT=123456
try :
    IP=sys.argv[1]
    PORT=sys.argv[2]
except Exception as e:
    print(e)
msg=""
try :
    for arg in sys.argv[3:]:
        msg=msg + str(arg) + " "
    msg=msg[:-1]
    #msg=sys.argv[3]
except Exception as e:
    print(e)
print(msg)
print(IP)
print(PORT)
msg=str(msg)
msg=str.encode(msg)
s = socket.socket()         # Create a socket object
s.connect((IP, int(PORT)))
s.sendall(msg)
s.close()                     # Close the socket when done
