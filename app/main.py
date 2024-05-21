#from os import confstr
import socket
import sys

class MyHTTPServer():
    def __init__(self) -> None:     
        self.status = ""
        self.headers = []
        self.body = ""
        server_socket = self.start_server()
        self.process_socket(server_socket=server_socket)


    def start_server(self):
        # Print statements for debugging
        # Create and configure the server socket
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        print("Server is listening on localhost:4221")
        return server_socket
    
    def process_socket(self,server_socket) -> None:
        while True:
            # Accept a client connection
            client_socket, __client_address = server_socket.accept()
            #print(f"Accepted connection from {client_address}")
            # Receive the request from the client, 1024 is the maximum buffsize
            request = client_socket.recv(1024).decode('utf-8')
            request_array = request.split()
            print("---------socket_start-----------")
            print(f"Received request:\n{request_array}")
            self.which_endpoint(request_array=request_array)
            self.build_response()
            # Send the response to the client
            client_socket.sendall(self.response.encode('utf-8'))
            print(f"Sent response:\n{self.response}")
            # Close the client connection
            client_socket.close()
            print("---------socket_closed-----------")

    def build_response(self) -> None:
        self.response = self.status
        if self.body != "":
            self.response += f"Content-Length {len(self.body)}\r\n{self.body}"
        for element in self.headers:
            self.response +=  f"{element}"
        self.response += "\r\n"
        

    def parse_body_content(self,request_array:list) -> str:
        content_start = -1
        for index,element in enumerate(request_array):
            if element in self.headers:
            #if element == "Content-Length:" or element == "Content-Type:":
                content_start = index+1 #maybe bug
        content = request_array[content_start:]
        result = ""
        if content:
            for elem in content:
                result = f"{result}{elem} "
            return result.rstrip()
        else:
            return ""

    def which_endpoint(self,request_array:list) -> None:
        """prepare http response"""
        path = request_array[1]
        action = request_array[0]
        self.get_compression_parameter(request_array=request_array)
        if path == "/":
            self.root_endpoint()
        elif path.startswith("/echo/"):
            self.echo_endpoint(path)
        elif path == "/user-agent":
            self.user_agent_endpoint(request_array=request_array)
        elif path.startswith("/files/") and action == "GET":
            self.get_file_endpoint(path)
        elif path.startswith("/files/") and action == "POST":
            self.post_file_endpoint(path,request_array=request_array)
        else:
            print("DEBUG: NO ENDPOINT FOUND")
            self.status = "HTTP/1.1 404 Not Found\r\n"

    def get_compression_parameter(self,request_array:list) -> None:
        not_allowed_compressions = ["invalid-encoding"]
        if "Accept-Encoding:" not in request_array:
            return
        for index,element in enumerate(request_array):
            if element == "Accept-Encoding:" and request_array[index+1] not in not_allowed_compressions:
                self.headers.append("Accept-Encoding:")
                self.headers.append(f"{request_array[index+1]}\r\n")

    def post_file_endpoint(self,path:str,request_array:list) -> None:
        content = self.parse_body_content(request_array=request_array)
        path_array = path.split("/")
        file = sys.argv[2] #this is the file path passed as a parameter
        file += path_array[-1]
        write_file(filename=file,content=content)
        self.status = "HTTP/1.1 201 Created\r\n"


    def get_file_endpoint(self,path:str) -> None:
        path_array = path.split("/")
        file = sys.argv[2]
        file += path_array[-1]
        content = read_file(filename=file)
        if content:
            self.status = "HTTP/1.1 200 OK\r\n"
            self.headers.append("Content-Type:") 
            self.headers.append("application/octet-stream\r\n")
            self.body = f"{content}"
        else:
            self.status = "HTTP/1.1 404 Not Found\r\n"


    def user_agent_endpoint(self,request_array:list) -> None:
        agent = ""
        for index,content in enumerate(request_array):
            if content == "User-Agent:":
                agent = request_array[index+1]
        self.status = "HTTP/1.1 200 OK\r\n"
        self.headers.append("Content-Type:") 
        self.headers.append("text/plain\r\n")
        self.body =  f"{agent}"

    def echo_endpoint(self,path:str) -> None:
        path_array = path.split("/")
        echo = path_array[-1]
        self.status = "HTTP/1.1 200 OK\r\n"
        self.headers.append("Content-Type:") 
        self.headers.append("text/plain\r\n")
        self.body = f"{echo}"

    def root_endpoint(self) -> None:
        self.status = "HTTP/1.1 200 OK\r\n"

def read_file(filename:str):
    try:
        with open(filename,"r") as file:
            return file.read()
    except FileNotFoundError:
        return False

def write_file(filename:str,content:str):
    with open(filename,"w+") as file:
        file.write(content)

def main():
    http = MyHTTPServer()
    http.start_server()

if __name__ == "__main__":
    main()

