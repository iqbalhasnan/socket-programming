#client that sent the file 
import os, struct, socket, sys


def main(host,port,inputfile):

    #prepare the packet to be sent
    with open(inputfile, 'rb') as file:
        data = file.read()
    # get the size of the image and pack it to 4-byte
    size = struct.pack('<I', os.path.getsize(inputfile))
    #format the filename to 20-byte and encode it
    filename = inputfile.rjust(20).encode()
    #packed all the bytes, 4-byte size, 20-byte filename, rest of image data
    packet = size + filename + data


    # create client socket.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect client socket to server
    client.connect((host, int(port)))
    #send packet 1024 at a time
    client.sendall(packet)
    #properly shutdown the client
    client.shutdown(socket.SHUT_RDWR)
    #close the client socket
    client.close()

if __name__ == '__main__':
    try:
        host = sys.argv[1] #remote host
        port = sys.argv[2] #port used by the server
        inputfile = sys.argv[3] #local filename
    except IndexError:
        print 'python ftpc.py <remote-IP> <remote-port> <local-file-to-transfer>'
        sys.exit(2)
    main(host,port,inputfile)