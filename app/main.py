import socket
import sys

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
    response = build_response(request_array=request_array)
    # Send the response to the client
    client_socket.sendall(response.encode('utf-8'))
    print("Sent response:\n" + response)
    # Close the client connection
    client_socket.close()

def build_response(request_array:str) -> str:
    """prepare http response"""
    path = request_array[1]
    if path == "/":
        response = root_endpoint()
    elif path.startswith("/echo/"):
        response = echo_endpoint(path)
    elif path == "/user-agent":
        response = user_agent_endpoint(request_array=request_array)
    elif path.startswith("/files/"):
        response = file_endpoint(path)
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    return response

def read_file(filename:str):
    try:
        with open(filename,"r") as file:
            return file.read()
    except FileNotFoundError:
        return False

def file_endpoint(path:str) -> str:
    path_array = path.split("/")
    file = sys.argv[2]
    file += path_array[-1]
    print(file)
    content = read_file(filename=file)
    if content:
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: application/octet-stream\r\n"
        response += f"Content-Length: {len(content)}\r\n"
        response += "\r\n"
        response += f"{content}\r\n"
        return response
    else:
        return "HTTP/1.1 404 Not Found\r\n\r\n"


def user_agent_endpoint(request_array:str) -> str:
    agent = ""
    for index,content in enumerate(request_array):
        if content == "User-Agent:":
            agent = request_array[index+1]
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/plain\r\n"
    response += f"Content-Length: {len(agent)}\r\n"
    response += "\r\n"
    response += f"{agent}\r\n"
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

