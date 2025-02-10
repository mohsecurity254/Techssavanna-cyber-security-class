import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a public host, and a well-known port
host = 'localhost'  # or any IP address you like
port = 12344  # replace with your chosen port number
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    print("Connected by", addr)

    # Receive data in a loop
    message = ""
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        message += data

    # Send back a response
    response = "You said: " + message
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()
