import numpy as np
import pandas as pd
from tqdm import tqdm
from rectools.models import PureSVDModel
from rectools import Columns
from rectools.dataset.dataset import Dataset
import pandas as pd
from flask import Flask, request
import json
import socket

def receive_file(client_socket, filell): 
    with open(filell , 'wb') as file: 
        while True: 
            data = client_socket.recv(1024) 
            if not data: 
                break 
            file.write(data)

class Algorithm:
    def fit_(self, port):
                    
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        host = '127.0.0.1' 
        server_socket.bind((host, port)) 
        server_socket.listen(50)
        client_socket, addr = server_socket.accept() 
        print(f"Connection from {addr}") 
        file_name = "data.csv" 
        print(f"Receiving file: {file_name}") 
        receive_file(client_socket, file_name) 
        print(f"File '{file_name}' received successfully.") 
        client_socket.close() 
            
        data = []
 
        with open("./data.csv", "r") as f: 
            lines = f.readlines() 
            for x in tqdm(lines): 
                movie_id, user_id, rating, date = x.split(",") 
                data.append((movie_id, int(user_id), int(rating), date))
         
        self.A = pd.DataFrame(data, columns=[Columns.User, Columns.Item, Columns.Weight, Columns.Datetime])
        self.dataset = Dataset.construct(self.A)
        self.model = PureSVDModel()
        self.model.fit(self.dataset)          
  

    def __init__(self):
        print("1")
        pass
        
        
    def predict_(self, user_id, k=10):
        recos = self.model.recommend(
            users=[user_id],
            dataset=self.dataset,
            k=k,
            filter_viewed=True,
        )                                     
        recos = recos[[Columns.Item, Columns.User]].values.tolist()
        return recos
      
    def run(self): 
        app = Flask(__name__)
        #run_with_ngrok(app)  
        @app.route('/predict', methods=['GET'])   
        def predict_n(): 
            if request.method == 'GET':
                user_id = int(request.args['user_id'])
                return json.dumps({"prediction": self.predict_(user_id)})
        
        @app.route('/fit', methods=['GET'])
        def fit_n():
            if request.method == 'GET':
                port = int(request.args['port'])
                print(port)
                self.fit_(port)
                return "200"

        app.run(port = 24567)
Algorithm().run()        