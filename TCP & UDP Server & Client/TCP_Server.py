import socket
import struct
import argparse

parser = argparse.ArgumentParser() # add a argument for running the file
parser.add_argument('port', type=int) # port argument
args = parser.parse_args()

def calculate(opCode, op1, op2):
    try:
        match(opCode):
            case 0:
                return op1 / op2
            case 1:
                return op1 * op2
            case 2:
                return op1 & op2
            case 3:
                return op1 | op2
            case 4:
                return op1 + op2
            case 5:
                return op1 - op2
        return None
    except Exception:
        return None
        


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Establish socket
server_socket.bind((socket.gethostname(), args.port)) #Bind port
server_socket.listen() 

while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024) #Recieve up to 1024 bytes
    ttl = struct.unpack('>H',data[0:2])[0] # > is for big edian and H is for 2 unsigned bytes
    opCode = struct.unpack('>B',data[2:3])[0] # B is for 1 unsigned byte
    op1 = struct.unpack('>h',data[3:5])[0] # h is for 2 signed bytes
    op2 = struct.unpack('>h',data[5:7])[0]
    requestId = struct.unpack('>B',data[7:8])[0]
    opNameLen = struct.unpack('>B',data[8:9])[0]
    opName = data[9:].decode('utf-16') # get rest of op name
    result = calculate(opCode, op1, op2)
    errorCode = 0
    if ttl != len(data):
        errorCode = 127
    if result == None:
        errorCode = 127
    print(f"Request Number: {requestId}\nOperation: {op1} {opName} {op2}")
    
    resp = struct.pack(">H B i B",8,requestId,result,errorCode) # structure the resonce to be 2 unsigned bytes, 1 unsigned byte, 4 signed bytes, 1 unsigned bytes
    client_socket.send(resp)
    client_socket.close()
