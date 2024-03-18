from flask import Flask, request
from flask_ngrok import run_with_ngrok
import json
import requests
from flask import jsonify
import socket



app = Flask(__name__)
# run_with_ngrok(app) 


data = {"url":["https://basilisk-relaxed-ghost.ngrok-free.app", "htttp:/localhost:8080"]}

with open('config.json', 'w') as outfile:
    json.dump(data, outfile)




class Ensembler:
    def __init__(self, a, callable):
        self.a = a
        self.callable = callable      
    def predict(self, data):   
        predicts = [x.predict(data) for x in self.a]
        return self.callable(predicts)
    def fit(self, data):   
        predicts = [x.predict(data) for x in self.a]
    def get_data(self):
        def receive_file(client_socket, filell): 
            with open(filell , 'wb') as file: 
                while True: 
                    data = client_socket.recv(1024) 
                    if not data: 
                        break 
                    file.write(data)
            # data_list = []
            # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #     s.connect(("127.0.0.1", 7000))
            #     data = s.recv(1024)
            #     data_list.append(data.decode())
            # return data_list  
        def main(): 
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            host = '127.0.0.1' 
            port = 5500
            server_socket.bind((host, port)) 
            server_socket.listen(50) 
            while True: 
                client_socket, addr = server_socket.accept() 
                print(f"Connection from {addr}") 
                file_name = "data.txt" 
                print(f"Receiving file: {file_name}") 
                receive_file(client_socket, file_name) 
                print(f"File '{file_name}' received successfully.") 
                client_socket.close() 
                return file_name
                
        if __name__ == "__main__": 
            main()
  


class connector:
    def __init__(self, url):
        self.url = url 
    def predict(self, user_id):
        data = {'user_id': user_id}
        response = requests.get(f"{self.url}/predict?user_id={user_id}").json()["prediction"]
        return response
    def fit(self, user_id):
        data = {'user_id': user_id}
        response = requests.get(f"{self.url}/predict?user_id={user_id}").json()["prediction"]
        

    
with open('config.json', 'r') as file:
    config_json = json.load(file)


connector_list = []
for url in config_json['url']:
    connector_instance = connector(url)  
    connector_list.append(connector_instance)


ensembler = Ensembler(connector_list, lambda x: x[0])

ensembler.get_data()


# request = requests.get("http://localhost:8080")

# with open('data.csv', 'r') as dat:
#     file_data = dat.read()
# for url in connector_list:
#     response = requests.post(url, data=file_data)


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
    app.run(host = '127.0.0.1', port = 5600)
