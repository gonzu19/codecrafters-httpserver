#from os import confstr
import socket
import sys
import gzip

class MyHTTPServer():
    def __init__(self) -> None:     
        server_socket = self.start_server()
        self.process_socket(server_socket=server_socket)

    def start_server(self):
        # Print statements for debugging
        # Create and configure the server socket
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        print("Server is listening on localhost:4221")
        return server_socket

    def reset_parameters(self) -> None:
        self.status = ""
        self.headers = []
        self.body = ""
        self.encoding = ""
        self.path = ""
        self.content_type = ""
    
    def process_socket(self,server_socket) -> None:
        while True:
            self.reset_parameters()
            # Accept a client connection
            client_socket, __client_address = server_socket.accept()
            #print(f"Accepted connection from {client_address}")
            # Receive the request from the client, 1024 is the maximum buffsize
            request = client_socket.recv(1024).decode('utf-8')
            self.request_array = request.split()
            print("---------socket_start-----------")
            print(f"Received request:\n{self.request_array}")
            self.which_endpoint()
            self.build_response()
            # Send the response to the client
            client_socket.sendall(self.response.encode('utf-8'))
            print(f"Sent response:\n{self.response}")
            # Close the client connection
            client_socket.close()
            print("---------socket_closed-----------")

    def build_response(self) -> None:
        print(f"debugg****{self.encoding}")
        self.response = self.status
        if self.body == "":
            self.response += "\r\n"
            return
        self.response += f"Content-Length: {len(self.body)}\r\n"
        self.response += f"Content-Type: {self.content_type}\r\n"
        if self.encoding != "":
            self.response += f"Content-Encoding: {self.encoding}\r\n"
        for element in self.headers:
            self.response +=  f"{element}"
        if "gzip" in self.encoding:
            compressed_body = gzip.compress(self.body.encode('utf-8'))
            self.response += f"{compressed_body.decode('utf-8')}"
        else:
            self.response += f"\r\n{self.body}"
        self.response += "\r\n"
        

    def parse_body_content(self) -> str:
        content_start = -1#placeholder
        header_names = ["Content-Length:","Accept-Encoding","Content-type","Agent-user"] #maybebug
        for index,element in enumerate(self.request_array):
            if element in header_names:
                content_start = index+2 
        content = self.request_array[content_start:]
        result = ""
        if content:
            for elem in content:
                result = f"{result}{elem} "
            return result.rstrip()
        else:
            return ""

    def which_endpoint(self) -> None:
        """prepare http response"""
        self.path = self.request_array[1]
        action = self.request_array[0]
        self.get_compression_parameter()
        if self.path == "/":
            self.root_endpoint()
        elif self.path.startswith("/echo/"):
            self.echo_endpoint()
        elif self.path == "/user-agent":
            self.user_agent_endpoint()
        elif self.path.startswith("/files/") and action == "GET":
            self.get_file_endpoint()
        elif self.path.startswith("/files/") and action == "POST":
            self.post_file_endpoint()
        else:
            print("DEBUG: NO ENDPOINT FOUND")
            self.status = "HTTP/1.1 404 Not Found\r\n"

    def get_compression_parameter(self) -> None:
        allowed_compressions = ["gzip"]
        if "Accept-Encoding:" not in self.request_array:
            return
        encoding_evaluation = False
        for element in self.request_array:
            stripped_element = element.rstrip(",")
            if element == "Accept-Encoding:":
                encoding_evaluation = True
            if encoding_evaluation and element != "Accept-Encoding:":
                if stripped_element in allowed_compressions:
                    if self.encoding == "":
                        self.encoding += stripped_element
                    else:
                        self.encoding += f",{stripped_element}"
                if element[-1] != ",":
                    return

    def post_file_endpoint(self) -> None:
        content = self.parse_body_content()
        path_array = self.path.split("/")
        file = sys.argv[2] #this is the file path passed as a parameter
        file += path_array[-1]
        write_file(filename=file,content=content)
        self.status = "HTTP/1.1 201 Created\r\n"


    def get_file_endpoint(self) -> None:
        path_array = self.path.split("/")
        file = sys.argv[2]
        file += path_array[-1]
        content = read_file(filename=file)
        if content:
            self.status = "HTTP/1.1 200 OK\r\n"
            self.content_type = "application/octet-stream"
            self.body = f"{content}"
        else:
            self.status = "HTTP/1.1 404 Not Found\r\n"


    def user_agent_endpoint(self) -> None:
        agent = ""
        for index,content in enumerate(self.request_array):
            if content == "User-Agent:":
                agent = self.request_array[index+1]
        self.status = "HTTP/1.1 200 OK\r\n"
        self.content_type = "text/plain"
        self.body =  f"{agent}"

    def echo_endpoint(self) -> None:
        path_array = self.path.split("/")
        echo = path_array[-1]
        self.status = "HTTP/1.1 200 OK\r\n"
        self.content_type = "text/plain"
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

