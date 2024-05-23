import unittest
import requests
#from app.main import MyHTTPServer
import os 

class TestHTTPServer(unittest.TestCase):

    def test_root_endpoint(self) -> None:
        """Test for: root_endpoint"""
        response = requests.get("http://localhost:4221/",verify=False)
        self.assertEqual(response.status_code,200)

    def test_echo_endpoint(self) -> None:
        """Test for: echo_endpoint"""
        response = requests.get("http://localhost:4221/echo/hola",headers={"Accept-Encoding": "compress"},verify=False)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.text,"hola")

    def test_file_endpoints(self) -> None:
        """Test for endpoints: post_file_endpoint, get_file_endpoint"""
        # Get the absolute path of the current script
        script_path = os.path.abspath(__file__)
        # Get the directory of the current script
        script_dir = os.path.dirname(script_path).rstrip("tests")
        post_response = requests.post("http://localhost:4221/files/pruebas.txt",headers={"Accept-Encoding": "compress"},verify=False,data="holamundo")
        self.assertEqual(post_response.status_code,201)
        self.assertEqual(os.path.exists(f"{script_dir}pruebas.txt"),True)
        get_response = requests.get("http://localhost:4221/files/pruebas.txt",headers={"Accept-Encoding": "compress"},verify=False)
        self.assertEqual(get_response.status_code,200)
        self.assertEqual(get_response.text,"holamundo")
        get_fail_response = requests.get("http://localhost:4221/files/doesnt_exit.txt",headers={"Accept-Encoding": "compress"},verify=False)
        self.assertEqual(get_fail_response.status_code,404)
        #delete the file
        os.remove(f"{script_dir}pruebas.txt")

    def test_user_agent_endpoint(self) -> None:
        """Test for: user_agent_endpoint"""
        response = requests.get("http://localhost:4221/user-agent",headers={"Accept-Encoding": "compress","User-Agent":"prueba"},verify=False)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.text,"prueba")
        
    def test_compression(self) -> None:
        """Test for: echo_endpoint,root_endpoint, using gzip compression"""
        response = requests.get("http://localhost:4221/echo/hi",headers={"Accept-Encoding": "gzip"},verify=False)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.headers.get("Content-Encoding"),"gzip")
        response = requests.get("http://localhost:4221/",headers={"Accept-Encoding": "gzip"},verify=False)
        self.assertEqual(response.status_code,200)
        #Here we should only get back the status code not the headers
        self.assertEqual(response.headers.get("Content-Encoding"),None)
        






if __name__ == '__main__':
    unittest.main()
