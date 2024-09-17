# import socket module
from socket import *
# In order to terminate the program
import sys


def webserver(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)  # This line allows the server to listen for incoming connections

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept the incoming connection

        try:
            # Receiving the client's message
            message = connectionSocket.recv(1024).decode()  # Decode the received message
            if not message:
                connectionSocket.close()
                continue

            filename = message.split()[1]  # Extract the filename from the request

            # Open the client-requested file
            with open(filename[1:], 'r') as f:  # Remove the leading "/" in the filename
                outputdata = f.read()  # Read the file content

            # Send HTTP response header
            response_header = "HTTP/1.1 200 OK\r\n"
            headers = (
                "Content-Type: text/html; charset=UTF-8\r\n" +
                "Server: MyPythonServer\r\n" +
                "Connection: close\r\n\r\n"
            )
            response = response_header + headers + outputdata

            # Send the HTTP response to the client
            connectionSocket.sendall(response.encode('utf-8'))  # Send everything at once

        except IOError:
            # Send HTTP response message for file not found
            response_header = "HTTP/1.1 404 Not Found\r\n"
            error_message = "<html><body><h1>404 Not Found</h1></body></html>"
            headers = (
                "Content-Type: text/html; charset=UTF-8\r\n" +
                "Server: MyPythonServer\r\n" +
                "Connection: close\r\n\r\n"
            )
            response = response_header + headers + error_message
            connectionSocket.sendall(response.encode('utf-8'))

        finally:
            # Close the client connection
            connectionSocket.close()


if __name__ == "__main__":
    webserver(13331)
