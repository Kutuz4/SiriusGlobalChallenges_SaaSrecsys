import pandas as pd
import numpy as np
import faiss
import math
import networkx as nx
import matplotlib.pyplot as plt
from flask import Flask, request
import json
import socket
from tqdm import tqdm


def receive_file(client_socket, filell): 
    with open(filell , 'wb') as file: 
        while True: 
            data = client_socket.recv(1024) 
            if not data: 
                break 
            file.write(data)

class Algorithm_graph:
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
        
        with open("./data3.csv", "r") as f:
            lines = f.readlines()
            for x in tqdm(lines):
                movie_id, user_id, rating, date = x.split(",")
                data.append((movie_id, int(user_id), int(rating), date))
        self.data = self.create_A(data)
        np.random.seed(50)
        self.G = self.create_G(self.data)
        self.bfs_films = np.zeros((len(self.G), len(self.G)))
        for i in range(len(self.G)):
            self.bfs_films[i] = self.bfs(self.G, i)
        
    def create_A(self, data):
        df = pd.DataFrame(data, columns=["movie_id", "user_id", "rating", "date"])
        df["user_index"] = df["user_id"].map({x: i for i, x in enumerate(df["user_id"].unique())})
        A = np.zeros((df["user_id"].nunique(), df["movie_id"].nunique()))
        for movie_id, user_id, rating in tqdm(df[["movie_id", "user_index", "rating"]].values):
            A[user_id, movie_id - 1] = rating
        return A
    
    def distance_matrix_function(self, data):
        distance_matrix = np.zeros((data.shape[1], data.shape[1]))
        lengths = [np.linalg.norm(data[:, i]) for i in range(data.shape[1])]
        dots = data.T @ data
        for i in range(data.shape[1]):
            for j in range(i + 1, data.shape[1]):
                distance_matrix[i, j] = dots[i, j] / (lengths[i] * lengths[j])
                distance_matrix[j, i] = distance_matrix[i, j]
        return distance_matrix
    
    def softmax_function(self, data):
        distance_matrix = self.distance_matrix_function(data)
        softmax = np.zeros((distance_matrix.shape[0], distance_matrix.shape[0]))
        exponenta = math.e ** ((distance_matrix - distance_matrix.mean()) / distance_matrix.std())
        for i in range(distance_matrix.shape[0]):
            sumznam = 0
            for j in range(distance_matrix.shape[0]):
                if i != j:
                    sumznam += exponenta[i][j]
            for j in range(distance_matrix.shape[0]):
                if i != j:
                    softmax[i][j] = (exponenta[i][j]) / sumznam
        return softmax
    
    def sample(self, probs, n): 
        V = [] 
        for i in range(n): 
            j = np.random.choice(len(probs), p=probs)
            probs[j] = 0
            probs /= probs.sum()
            V.append(j)
        return V
    
    def create_G(self, data):
        softmax = self.softmax_function(data)
        G = nx.Graph()
        for i in range(softmax.shape[0]):
            k = self.sample(softmax[i], 3)
            for j in range(3):
                G.add_edge(i, k[j])
        return G
    
    def bfs(self, G, idonegoodfilm):
        queue, visit = [idonegoodfilm], {idonegoodfilm}
        distances = np.zeros(self.G.number_of_nodes())
        while queue:
            m = queue.pop(0)
            for neighbour in G[m]:
                if neighbour not in visit:
                    visit.add(neighbour)
                    queue.append(neighbour)
                    distances[neighbour] = distances[m] + 1
        return distances
    
    def __init__(self):
        print("1")
        pass
        
    
    def rec(self, ratings, id):
        idgoodfilms, distance_films = [], []
        for i in range(len(ratings[id])):
            if ratings[id][i] >= 4:
                idgoodfilms.append(i)
        distance_films = self.bfs_films[idgoodfilms]
        rec_films = []
        if len(distance_films) == 0:
            for h in range(len(ratings[id])):
                if ratings[id][h] == 0:
                    rec_films.append((ratings[ratings[:, h] > 0, h].mean(), h))
            return sorted(rec_films)[::-1]
        else:
            indices = np.arange(0, len(distance_films[0]))
            indices = indices[ratings[id] == 0]
            rec_films = list(map(lambda x: (x[0], int(x[1])), zip(distance_films[:, indices].mean(axis=0), indices)))
            return sorted(rec_films)
    
    def predict(self, id, k=100):
        return self.rec(self.data, id)[:k]
    
    def run(self): 
        app = Flask(__name__)
        #run_with_ngrok(app)
        @app.route('/predict', methods=['GET'])   
        def predict_n(): 
            if request.method == 'GET':
                user_id=int(request.args['user_id'])
                return json.dumps({"prediction": self.predict(user_id)})
            
        @app.route('/fit', methods=['GET'])
        def fit_n():
            if request.method == 'GET':
                port = int(request.args['port'])
                print(port)
                self.fit_(port)
                return "200"    
        
        app.run()
Algorithm_graph().run()
