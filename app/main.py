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

        # Receive the request from the client, 1024 is the maximum buffsize
        request = client_socket.recv(1024).decode('utf-8')
        request_array = request.split()
        print(f"Received request:\n{request}")

        # Prepare an HTTP response
        if request_array[1] == "/":
            response = "HTTP/1.1 200 OK\r\n"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"


        # Send the response to the client
        client_socket.sendall(response.encode('utf-8'))
        print("Sent response:\n" + response)

        # Close the client connection
        client_socket.close()

if __name__ == "__main__":
    main()

