#server that receive the file
import socket, struct,sys

def main(port):
    #create new server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #bind port
    server.bind(('164.107.112.73', int(port)))
    #set max accept rate to 5 conenctions
    server.listen(5)
    #server socket accept the client
    client, address = server.accept()
    #get 4-byte packet
    size_bytes = client.recv(4)
    #unpack 4-byte packet that determine the size of image
    size = struct.unpack('<I', size_bytes)[0]
    #decode the 20-byte that determine the filename and strip the space
    filename =  client.recv(20).decode().lstrip()
    #get the remaining image bytes from client
    get_bytes(client, size, filename)
    # Shutdown the socket and close the server conenction.
    server.shutdown(socket.SHUT_RDWR)
    server.close()
    #print the status
    print('Server has received the data from the client! ')

#method to get the image bytes from client to the server
def get_bytes(sock, size, filename):
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
        #immediately write the bytes received to the file in current server directory
        with open(filename, 'wb') as file:
            file.write(packet)

if __name__ == '__main__':
    try:
        port = sys.argv[1] 
    except IndexError:
        print 'python ftps.py <local-port>'
        sys.exit(2)
    main(port)
