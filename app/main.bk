import socket

def start_server():
    # Print statements for debugging
    print("Server is starting...")
    # Create and configure the server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on localhost:4221")
    return server_socket
    
def process_socket(server_socket) -> None:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    # Receive the request from the client, 1024 is the maximum buffsize
    request = client_socket.recv(1024).decode('utf-8')
    request_array = request.split()
    print(request_array)
    print(f"Received request:\n{request}")
    path = request_array[1]
    response = build_response(path=path)
    # Send the response to the client
    client_socket.sendall(response.encode('utf-8'))
    print("Sent response:\n" + response)
    # Close the client connection
    client_socket.close()

def build_response(path:str) -> str:
    """prepare http response"""
    if path == "/":
        response = root_endpoint()
    elif path.startswith("/echo/"):
        response = echo_endpoint(path)
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    return response


def echo_endpoint(path:str) -> str:
    path_array = path.split("/")
    echo = path_array[-1]
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/plain\r\n"
    response += f"Content-Length: {len(echo)}\r\n"
    response += "\r\n"
    response += f"{echo}\r\n"
    return response

def root_endpoint() -> str:
    response = "HTTP/1.1 200 OK\r\n\r\n"
    return response

def main():
    server_socket = start_server()
    while True:
        process_socket(server_socket)

if __name__ == "__main__":
    main()

