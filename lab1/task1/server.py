import socket
import threading
from datetime import datetime
import time

# Налаштування хоста
host = '127.0.0.1'
port = 20300

# Глобальна змінна для контролю роботи сервера
run_server = True


# Обробник клієнта
def handle_client(client_socket, addr):
    global run_server
    print(f"З'єднання з {addr} встановлено.")

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            # Декодування отриманого повідомлення
            message = data.decode('utf-8')
            print(f"Отримано ({addr}): {message} о {datetime.now()}")

            # Якщо отримано команду вимкнення сервера
            if message.lower() == 'shutdown':
                print("Отримано команду вимкнення сервера.")
                run_server = False
                break

            # Симуляція затримки
            time.sleep(5)

            # Відправлення відповіді (відлуння)
            sent = client_socket.send(data)
            if sent == 0:
                raise RuntimeError("Сокетне з'єднання перервано")

            print(f"Відлуння відправлено до ({addr}) о {datetime.now()}")

        except socket.error as e:
            print(f"Помилка сокета: {e}")
            break

    # Закривання з'єднання
    client_socket.close()
    print(f"З'єднання з {addr} закрите.")


# Створення сокету та прослуховування вхідних підключень
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Сервер чекає на підключення на {host}:{port}...")

    while run_server:
        try:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
        except Exception as e:
            print(f"Виникла помилка: {e}")
            break

    server_socket.close()
