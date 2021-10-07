from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 6789))
serverSocket.listen(1)
while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        #print(message)
        endPoint = message.split()[1]
        print(endPoint)
        filename = '/default.html'
        f = open(filename[1:], 'rb')
        outputdata = f.read()
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
        connectionSocket.send(outputdata)
        connectionSocket.send('\r\n'.encode())
        connectionSocket.close()
    except IOError:
        print('transmisission error')
        connectionSocket.close()
serverSocket.close()
sys.exit()