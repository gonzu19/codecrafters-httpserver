import socket

def main():
    # Print statements for debugging
    print("Server is starting...")

    # Create and configure the server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    print("Server is listening on localhost:4221")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Receive the request from the client
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")

        # Prepare an HTTP response
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: 13\r\n"
        response += "\r\n"
        response += "Hello, world!"

        # Send the response to the client
        client_socket.sendall(response.encode('utf-8'))
        print("Sent response:\n" + response)

        # Close the client connection
        client_socket.close()

if __name__ == "__main__":
    main()

