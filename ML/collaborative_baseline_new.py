import pandas as pd
import numpy as np
import faiss
from flask import Flask, request
import json

def nonzero_mean(A):
    vector = []
    for i in range(A.shape[1]):
        sum, k = 0, 0
        for j in range(A.shape[0]):
            if A[j][i] != 0:
                sum += A[j][i]
                k += 1
        vector.append(sum/(k + 1e-9))
    return vector

class Algorithm:

    def create_A(self, data):
        df = pd.DataFrame(data, columns=["movie_id", "user_id", "rating", "date"])
        df["user_index"] = df["user_id"].map({x: i for i, x in enumerate(df["user_id"].unique())})
        A = np.zeros((df["user_id"].nunique(), df["movie_id"].nunique()))
        for movie_id, user_id, rating in tqdm(df[["movie_id", "user_index", "rating"]].values):
            A[user_id, movie_id - 1] = rating
        return A

    def fit_(self, port):
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        host = '127.0.0.1' 
        server_socket.bind((host, port)) 
        server_socket.listen(50)
        client_socket, addr = server_socket.accept() 
        print(f"Connection from {addr}") 
        file_name = "data4.csv" 
        print(f"Receiving file: {file_name}") 
        receive_file(client_socket, file_name) 
        print(f"File '{file_name}' received successfully.") 
        client_socket.close() 
        
        data = []
 
        with open("./data4.csv", "r") as f: 
            lines = f.readlines() 
            for x in tqdm(lines): 
                movie_id, user_id, rating, date = x.split(",") 
                data.append((movie_id, int(user_id), int(rating), date))

        self.A = self.create_A(data)
        self.index = faiss.IndexFlatIP(4499)
        self.index.add(self.A)

    def __init__(self):
        pass
        
        
    def predict_(self, user_id, k=10):                                     
        y_pred = self.index.search(np.reshape(self.A[user_id], (1, -1)), k)
        F = y_pred[1]
        F = F[:, 1:]
        y_pred_1 = nonzero_mean(self.A[F][0])
        return y_pred_1 
      
    def run(self): 
        app = Flask(__name__)
        #run_with_ngrok(app)
        @app.route("/")   
        @app.route('/predict', methods=['GET'])   
        def predict_n(): 
            if request.method == 'GET':
                user_id=int(request.args['user_id'])
                return json.dumps({"prediction": self.predict_(user_id)})
        app.run()

Algorithm().run()
