import socket
import threading

print("\n mnbv Talk \n")
ip_option = input("1. mnbv '127.0.0.1:63900'\n2. test@test '127.0.0.1:63901'\n3. Alt 'IP:Port'\n: ")

try:
    if ip_option == '1':
        host = '127.0.0.1'
        port = 63900
    elif ip_option == '2':
        host = '127.0.0.1'
        port = 63901
    else:
        custom_ip = input("drop 'IP:Port': ").split(':')
        host = custom_ip[0]
        port = int(custom_ip[1])

except Exception as e:
    print("no options, sort it")
    exit(1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

connected_clients = {} # dict
stop_server = threading.Event()

def handle_client(client_socket, username):
    try:
        broadcast_msg = f"{username} joined chat"
        for client in connected_clients:
            if client != username:
                connected_clients[client].send(broadcast_msg.encode())

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            for client in connected_clients:
                if client != username:
                    message = f"{username}: {data}"
                    connected_clients[client].send(message.encode())
                    print(f"{username} Msg innit...")

    except Exception as e:
        print(f"{username} exited chat {addr[0]}:{addr[1]} unexpected") # {e}

    finally:
        if username in connected_clients:
            del connected_clients[username]
            leave_msg = f"{username} left chat"
            for client in connected_clients:
                connected_clients[client].send(leave_msg.encode())

def server_shutdown():
    print("shutting-down-server\nNo-more-cypher-allowed")
    stop_server.set()
    server_socket.close()
    exit(1)

while not stop_server.is_set():
    try:
        client, addr = server_socket.accept()
        print(f"accepted connection from: {addr[0]}:{addr[1]}")
        
        username = client.recv(1024).decode()
        connected_clients[username] = client
        client_handler = threading.Thread(target=handle_client, args=(client, username))
        client_handler.start()

    except KeyboardInterrupt:
        server_shutdown()
        exit(1)

    except Exception as e: # ~!
        print(f"error accepting conn...: {e}")
        exit(1)

    finally:
        print(f"{username} connected::{addr[0]}:{addr[1]}")

server_shutdown()
