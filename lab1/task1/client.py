import socket

# Налаштування хоста
host = '127.0.0.1'
port = 20300

# Створення сокету
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))  # Підключення до сервера
    while True:
        text_to_send = input("Введіть текст для відправлення або 'exit' для виходу: ")
        if text_to_send.lower() == 'exit':
            break
        s.sendall(text_to_send.encode('utf-8'))  # Відправлення тексту серверу

        # Очікування відповіді від сервера
        data = s.recv(1024)
        print(f"Відлуння від сервера: {data.decode('utf-8')}")
