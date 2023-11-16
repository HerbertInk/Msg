import socket
import threading

def connect_to_server():
    print("\n MNBV Talk \n")
    server_option = input("1. mnbv-server-1  127.0.0.1:63900\n2. Alt IP:Port\n use port 63903: ")

    try:
        if server_option == '1':
            server_host = '127.0.0.1'
            server_port = 63900
        else:
            custom_server = input("drop IP:Port: ").split(':')
            server_host = custom_server[0]
            server_port = int(custom_server[1])

    except Exception as e:
        print("no options, sort it")
        exit(1)

    return server_host, server_port

server_host, server_port = connect_to_server()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_host, server_port))

except ConnectionRefusedError:
    print("adjust addrss sequence")
    exit(1)

username = input("---drop username, no cap---: ")
client_socket.send(username.encode())

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message: # ~!
                print("server-conn-terminated")
                client_socket.close()
                break
            else:
                print(message)

        except:
            print("server-conn-reset")
            client_socket.close()
            exit(1)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

try:
    while True:
        message = input()
        client_socket.send(message.encode())

except KeyboardInterrupt:
    print("you-exited-chat")

finally: # will-exit
    client_socket.send(b'exit-at-will') 
    client_socket.close()
    receive_thread.join()
