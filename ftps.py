#server that receive the file
import socket, struct,sys

def main(port):
    #create new server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind port
    server.bind(('164.107.112.73', int(port)))
    #set max accept rate to 10 conenctions
    server.listen(5)
    #server socket accept the client
    client, address = server.accept()
    #get 4-byte packet
    packet = get_bytes(client, struct.calcsize('<I'))
    #unpack 4-byte packet that determine the size of image
    size = struct.unpack('<I', packet)[0]
    #decode the 20-byte that determine the filename and strip the space
    filename =  client.recv(20).decode().lstrip()
    #get the image data from client
    image = get_bytes(client, size)
    # Shutdown the socket and close the server conenction.
    server.shutdown(socket.SHUT_RDWR)
    server.close()
    #print the status
    print('Server is receiving the data from client :)')
    #write the image received to the current server directory
    with open(filename, 'wb') as file:
        file.write(image)

#method to return the number of bytes from client to the server
def get_bytes(sock, size):
    packet = bytearray()
    # Loop until all expected data is received.
    while len(packet) < size:
        #store the bytes in the buffer
        buffer = sock.recv(size - len(packet))
        if not buffer:
            # throw an exception if could not get all the data
            raise EOFError('Could not receive all expected data!')
        #append buffer into packet
        packet.extend(buffer)
        #return the bytes packet
    return bytes(packet)

if __name__ == '__main__':
    try:
        port = sys.argv[1] 
    except IndexError:
        print 'python ftps.py <local-port>'
        sys.exit(2)
    main(port)