import socket
import struct
import argparse

# Team Number = 6
# python ServerUDP.py 10016

def calculate(opCode,operand1,operand2):
    """Calculates expression based on given opCode

    Args:
        opCode (int): Number between 0-5 that tells what operation should be preformed
        operand1 (int): The first number in the operation
        operand2 (int): The second number in the operation
    Returns:
        int: Result of calculated expression
    """    
    result = 0
    match opCode:
        case 0:
            result = operand1 / operand2
        case 1:
            result = operand1 * operand2
        case 2:
            result = operand1 & operand2
        case 3:
            result = operand1 | operand2
        case 4:
            result = operand1 + operand2
        case 5:
            result = operand1 - operand2
        case _:
            result = -1
    return result

def getOpCodeOp(opCode):
    """Gets the operator represented by opCode

    Args:
        opCode (int): Number between 0-5 that tells what operation should be preformed

    Returns:
        str: Operator Char representation
    """    
    result = ''
    match opCode:
        case 0:
            result = '/'
        case 1:
            result = '*'
        case 2:
            result = '&'
        case 3:
            result = '|'
        case 4:
            result = '+'
        case 5:
            result = '-'
        case _:
            result = '-1'
    return result

def formatReply(result,requestId, errorCode):
    """_summary_

    Args:
        result (int): Result of claculated expression
        requestId (str): The number request this client has made to the server
        errorCode (int): Error code of calculation

    Returns:
        Bytes: Responce message encoded
    """    
    reply = struct.pack('!H B i B', 8, requestId, result, errorCode)
    return reply

def printBytes(hexMessage):
    """Prints all hex values in given message

    Args:
        hexMessage (str): Hex Values in message
        direction (int): Used for dialog options
    """      
    print('Bytes in order of recieved: ')
    for i in range(0, len(hexMessage), 2):
        byte = hexMessage[i:i+2]
        print(f'Byte {int(i/2)}: {byte}')
            

def startServer(port):
    """Starts the server that listens on given port for messages

    Args:
        port (int): Port recieved from Args

    Raises:
        Can Not Divide By 0: Message tried to divide by 0
        The Result Of The Calculations Was Too Big To Send: Calculation was bigger then mesage can send
    """    
    udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Creates a socket with socket.AF_INET being IPV4 and socket.SOCK_DGRAM being a datagram
    udpServer.bind((socket.gethostname(), port)) #Binds socket to a port
    print(f'UDP Server Binded to Port ${port}')
    
    while True:
        try: #Tries to get messages
            
            rawMessage, clientAddress = udpServer.recvfrom(1024) #Waits and recieves a message from a client
            print(f'Received message from {clientAddress[0]}')
            
            errorCode = 0
            tml = struct.unpack('!H', rawMessage[0:2])[0] #Gets information from recieved message
            opCode = struct.unpack('!B', rawMessage[2:3])[0]
            operand1 = struct.unpack('!h', rawMessage[3:5])[0]
            operand2 = struct.unpack('!h', rawMessage[5:7])[0]
            requestId = struct.unpack('!B', rawMessage[7:8])[0]
            opNameLength = struct.unpack('!B', rawMessage[8:9])[0]
            
            
            try:#Incase opNameLength is wrong
                opName = rawMessage[9:9 + (opNameLength * 2)].decode('utf-16') #Gets the operation name with variable size 
            except Exception as f:
                print(f'Error unpacking operationName: {f}')
                errorCode = 127
                   
        except Exception as e:
            print(f'Error unpacking message: {e}')
            errorCode = 127
            
            
        printBytes(rawMessage.hex())
        print(f'Client Requested The Operation:( {operand1} {getOpCodeOp(opCode)} {operand2} ) With Request ID: {requestId}')
        
        
        try: #Catches Calculation Errors
            if operand2 == 0 and opCode == 0:
                result = 0
                errorCode = 127
                raise Exception('Can Not Divide By 0')
            else:
                result = calculate(opCode,operand1,operand2)
            if result < -2147483648 or result > 2147483647:
                raise Exception(f'The Result Of The Calculations Was Too Big To Send: {result}')
        except Exception as e:
            print(f'Error Calculating Result: {e}')
            errorCode = 127
            
            
        try: #Catches errors sending message
            reply = formatReply(int(result),requestId, errorCode)
            udpServer.sendto(reply,clientAddress)
        except Exception as e:
            print(f'Something Went Wrong: {e}')       
            
if __name__ == '__main__':
    """Starts Server
    """    
    parser = argparse.ArgumentParser() #Grabs arguments
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    startServer(args.port)
