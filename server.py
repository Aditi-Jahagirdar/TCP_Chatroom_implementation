import socket
import threading

host =  '127.0.0.1'
port = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

#broadcast method sends message to all clients currently connected to the server
def broadcast(message):
    for client in clients:
        client.send(message)
        
#handle method receives message from client , process the message and broadcast the response to all clients connected to server
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname =nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break
            
#receive method combines other methods
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        #server asks client for nickname throgh a keyword 'NICK'
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))
        
        thread =threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening..')
receive()
