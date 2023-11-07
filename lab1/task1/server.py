import socket
from datetime import datetime

# Налаштування хоста
host = '127.0.0.1'
port = 20300

# Створення сокету
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))  # Зв'язування сокету з хостом
    s.listen()            # Перевід сокету в режим очікування
    print(f"Сервер на {host}:{port}")

    conn, addr = s.accept()  # Очікування на підключення
    with conn:
        print(f"З'єднано з {addr}")
        while True:
            data = conn.recv(1024)  # Прийом даних від клієнта
            if not data:
                break

            received_text = data.decode('utf-8')
            print(f"Отримано о {datetime.now()}: {received_text}")
