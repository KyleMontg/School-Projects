import socket
import struct
import argparse
import time

# Team Number = 6
# python ClientUDP.py ServerIP/HostName 10016

def packMessage(opCode, operand1, operand2, requestId):
    """Encodes a message to be sent to a server

    Args:
        opCode (int): Number between 0-5 that tells what operation should be preformed
        operand1 (int): The first number in the operation
        operand2 (int): The second number in the operation
        requestId (str): The number request this client has made to the server

    Returns:
        Bytes: An encoded packet containing information on operation
    """    
    operationNames = ['div','mul','and','or','add','sub']
    opName = operationNames[opCode]
    opNameEncoded = opName.encode('utf-16be') #Encodes in Big Endian
    opNameLength = len(opNameEncoded) + 2 # Adds the length of the encoded name + 2 for the BOM
    tml = 9 + opNameLength
    packedMessage = struct.pack('!H B h h B B', tml, opCode, operand1, operand2, requestId, opNameLength) # Packages the information with an ecoding scheme that defines how many bytes per variable
    packedMessage += b'\xfe\xff' + opNameEncoded # Adding BOM
    return packedMessage

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

def getInputs():
    """_summary_

    Raises:
        invalid input: Raised if byte representation of number would not fit in encoded message
    Returns:
        int: Numbers user wants to use for operation
    """    
    opCode = -1
    operand1 = -1
    operand2 = -1

    while True :
        try:
            opCode = int(input('OpCode:     | 0 | 1 | 2 | 3 | 4 | 5 | \n            -------------------------\nOperation:  | / | * | & | | | + | - | \nEnter The Operation Code Of The Operation You Want To Conduct: '))
            if 0 <= opCode <= 5:
                break
            else:
                raise Exception('invalid input')
        except Exception as e:
            print('Please Enter A Valid Operation Code!')

    while True :
        try:
            operand1 = int(input('Enter The First Whole Number Between -32768 to 32767: '))
            if -32768 <= operand1 <= 32767:
                break
            else:
                raise Exception('invalid input')
        except Exception as e:
            print('Please Enter A Valid Number!')
            
    while True :
        try:
            operand2 = int(input('Enter The Second Whole Number Between -32768 to 32767: '))
            if -32768 <= operand2<= 32767:
                break
            else:
                raise Exception('invalid input')
        except Exception as e:
            print('Please Enter A Valid Number!')
            
    return opCode,operand1,operand2

def printBytes(hexMessage, direction):
    """Prints all hex values in given message

    Args:
        hexMessage (str): Hex Values in message
        direction (int): Used for dialog options
    """    
    if direction == 1 :
        print('Bytes In Order Of Sent: ')
    else:  
        print('Bytes In Order Of Recieved: ')
    for i in range(0, len(hexMessage), 2):
        byte = hexMessage[i:i+2]
        print(f'Byte {int(i/2)}: {byte}')
            
def again(opCode, operand1, operand2, tml, responceId, result, errorCode, timeSent, timeBack):
    """Displays information about responce and checks if user wants to do another calcualtion

    Args:
        opCode (int): Number between 0-5 that tells what operation should be preformed
        operand1 (int): The first number in the operation
        operand2 (int): The second number in the operation
        tml (int): Total message length
        requestId (str): The number request this client has made to the server
        result (int): Result of claculation recieved
        errorCode (int): Error code recieved
        timeSent (int): Time message was sent
        timeBack (int): Time message was recieved

    Raises:
        Exception: Checks if valid input

    Returns:
        bool: If user wants to send another message
    """    
    print(f'The Request Number: #{responceId} Finished in {(timeBack-timeSent)*1000:.3f} ms And Has Returned With An Error Code Of: {'Ok' if errorCode == 0 else errorCode}')
    print(f'The Result Of The Calculation: ( {operand1} {getOpCodeOp(opCode)} {operand2} ) = {result}')
    while True :
        try:
            another = int(input(f'Would You Like To Send Another Message? Enter 1 if YES, Enter 2 if No: '))
            if 1 <= another <= 2:
                break
            else:
                raise Exception('invalid input')
        except Exception as e:
            print('Please Enter A Valid Responce!')
    return True if another == 1 else False

   
    
def startClient(ip, port):
    """Runs the client server and handles sending and reciving messages

    Args:
        ip (int): server ip
        port (int): port to connect to 
    """    
    cont = True
    requestId = 1
    while cont:
        opCode, operand1, operand2 = getInputs()
        udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Creates a socket with socket.AF_INET being IPV4 and socket.SOCK_DGRAM being a datagram
        message = packMessage(opCode, operand1, operand2, requestId)
        printBytes(message.hex(),1)
        requestId += 1 
        timeSent = time.perf_counter() #Time just before sending message
        udpClient.sendto(message, (ip, port)) #Uses created used socket to send the message to the servers ip on int port
        try: #Trys to listen for a responce
            rawResponse, server_address = udpClient.recvfrom(1024)
        except Exception as e:
            print(f'Error: {e}') #Used incase server send a bad packet
        timeBack = time.perf_counter() #Time right after receiving message
        try:
            printBytes(rawResponse.hex(),0)
        except Exception as e:
            print('Could Not Find Server')
        tml = struct.unpack('!H', rawResponse[0:2])[0] #Gets information from recieved message
        responceId = struct.unpack('!B', rawResponse[2:3])[0]
        result = struct.unpack('!i', rawResponse[3:7])[0]
        errorCode = struct.unpack('!B', rawResponse[7:8])[0]
        cont = again(opCode, operand1, operand2, tml, responceId, result, errorCode, timeSent, timeBack)
    

if __name__ == '__main__':
    """Runs on file execution
    """    
    parser = argparse.ArgumentParser() #Processes arguments
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    startClient(args.ip, args.port) #Starts client
