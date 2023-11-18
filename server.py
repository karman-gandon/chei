import socket
import threading

# Определение локального IP-адреса
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"Server IP: {local_ip}")

# Создание сокета для сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((local_ip, 5555))  # Привязка к локальному IP и порту 5555
server_socket.listen(5)

clients = []
hair_count = 0

def handle_client(client):
    global hair_count
    while True:
        try:
            data = client.recv(1024)
            if data:
                message = data.decode()
                if message.startswith('Clicked'):
                    hair_count += 1
                    print(f"New hair count: {hair_count}")
                    broadcast(f"Hair count: {hair_count}".encode())
                else:
                    broadcast(message.encode())
        except:
            clients.remove(client)
            client.close()
            break

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()
            clients.remove(client)

# Бесконечный цикл для прослушивания подключений
while True:
    client, addr = server_socket.accept()
    clients.append(client)
    print(f"Connection established with {addr}")
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
