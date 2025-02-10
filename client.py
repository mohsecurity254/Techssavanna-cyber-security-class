import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
host = 'localhost'  # or any IP address you like
port = 12344  # replace with your chosen port number
client_socket.connect((host, port))

# Send data
message = "Hello Server!"
client_socket.sendall(message.encode('utf-8'))

# Receive data from server and print it
data = client_socket.recv(1024).decode('utf-8')
print("Received:", data)

# Close the socket
client_socket.close()
