import socket
import threading

# Вибір нікнейму
nickname = input("Виберіть свій нікнейм: ")

# Підключення до сервера
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

# Прийняття повідомлень
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Помилка!")
            client.close()
            break

# Відправлення повідомлень
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Запуск потоків для прийняття та відправлення повідомлень
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
