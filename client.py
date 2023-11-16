import socket
import threading

def connect_to_server():
    print("\n MNBV Talk \n")
    server_option = input("1. mnbv-server-1  127.0.0.1:63900\n2. Alt IP:Port\n use port 63903: ")
    """
        The mnbv-servers are for testing on localhost
        use server ip address for an alternative configuration.
        Clients on the network initiate connection to a server via 
        the server's ip address and a dedicated port.
    """
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
        """
            this 'while' loop enables clients to 
            receive messages on a network
        """
        try:
            message = client_socket.recv(1024).decode()
            """
                1024 maximum amount of data (in bytes)
                transmitted on a network
            """
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
            """
                on chat exit, the client socket is closed
                Ctrl+C exits a user from chat
            """

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

try:
    while True:
        message = input()
        client_socket.send(message.encode())
        """
            this 'while' loop enables clients to 
            send a message on a network
        """

except KeyboardInterrupt:
    print("you-exited-chat")

finally: # will-exit
    client_socket.send(b'exit-at-will') 
    client_socket.close()
    receive_thread.join
    """
        a message of a connection drop
        is broadcast to clients on a network
        when a client exits wilingly by pressing 'Ctrl+C'
    """
