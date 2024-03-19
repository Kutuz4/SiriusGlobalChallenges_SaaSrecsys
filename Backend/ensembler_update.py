from flask import Flask, request
from flask_ngrok import run_with_ngrok
import json
import requests
from flask import jsonify
import numpy as np
import socket
import time


def receive_file(client_socket, filell): 
    with open(filell , 'wb') as file: 
        while True: 
            data = client_socket.recv(1024) 
            if not data: 
                break 
            file.write(data)

def send_file(server_socket, file_name):
    with open(file_name, 'rb') as file:
        for data in iter(lambda: file.read(1024), b''):
            server_socket.sendall(data)
            
def delete_port(url):
    return url.rstrip("1234567890").strip(":")

def extract_port(url):
    return int(url.split(":")[-1])
            

app = Flask(__name__)
# run_with_ngrok(app) 


#data = {"url":["https://basilisk-relaxed-ghost.ngrok-free.app", "http://127.0.0.1:5000"], "database_url": "http://127.0.0.1:7000"}
data = {"url":["127.0.0.1:24567"], "database_url": "127.0.0.1:6000"}

with open('config.json', 'w') as outfile:
    json.dump(data, outfile)



class Ensembler:
    def __init__(self, a, callable, database_url):
        self.a = a
        self.callable = callable      
        self.database_url = database_url
        
    def predict(self, data):   
        predicts = [x.predict(data) for x in self.a]
        return self.callable(predicts)
    
    def fit(self):  
        for x in self.a:
            x.fit()
        
    def get_data(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        host = delete_port(self.database_url)
        port = np.random.randint(low=20000, high=25000)
        try:
            requests.get(f"http://{self.database_url}/getdata?port={port}", timeout=0.1)
        except:
            pass
        server_socket.bind((host, port))    
        server_socket.listen(50)
        
        client_socket, addr = server_socket.accept() 
        print(f"Connection from {addr}") 
        file_name = "data.csv" 
        print(f"Receiving file: {file_name}")
        receive_file(client_socket, file_name)
        print(f"File '{file_name}' received successfully.") 
        client_socket.close() 
        return file_name
  


class connector(Ensembler):
    def __init__(self, url, data_file_name):
        self.url = url
        self.data_file_name = data_file_name
        
    def predict(self, user_id):
        data = {'user_id': user_id}
        response = requests.get(f"{self.url}/predict?user_id={user_id}").json()["prediction"]
        return response
    
    def fit(self): 
        host = delete_port(self.url)
        port = np.random.randint(low=20000, high=25000)
        print(port)
        print(self.url)
        print(host)
        try:
            r = requests.get(f"http://{self.url}/fit?port={port}", timeout=0.1)
        except:
            pass
        time.sleep(10)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        send_file(client_socket, "data.csv")
        client_socket.close()

    
with open('config.json', 'r') as file:
    config_json = json.load(file)

data_file_name = "data.csv"
connector_list = []
for url in config_json['url']:
    connector_instance = connector(url, data_file_name) 
    connector_list.append(connector_instance)


ensembler = Ensembler(connector_list, lambda x: x[0], config_json["database_url"])
ensembler.get_data()
ensembler.fit()





@app.route('/predict', methods = ['POST', 'GET'])
def answer():
    if request.method == 'POST':
        data = request.post('data')
        prediction = ensembler.predict(data)
        return json.dumps({"prediction": prediction})
    if request.method == 'GET': 
        user_id = request.args.get('user_id')
        prediction = ensembler.predict(user_id)
        return json.dumps({"prediction": prediction})
    
        
           
if __name__ == "__main__":
    app.run(port = 7000)
