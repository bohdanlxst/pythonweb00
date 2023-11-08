import socket
import threading

# Параметри сокета
host = '127.0.0.1'
port = 12345

# Створення серверного сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen()

# Список клієнтів і нікнеймів
clients = []
nicknames = []

# Надсилання повідомлень всім клієнтам
def broadcast(message):
    for client in clients:
        client.send(message)

# Обробка повідомлень від клієнтів
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} вийшов з чату!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Прийняття нових з'єднань
def receive():
    while True:
        client, address = server_socket.accept()
        print(f"Підключено з {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Нікнейм користувача: {nickname}')
        broadcast(f'{nickname} приєднався до чату!'.encode('utf-8'))
        client.send('Підключено до сервера!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Сервер активовано і слухає...")
receive()
