import pandas as pd
import numpy as np
import faiss
from flask import Flask, request
from flask_ngrok import run_with_ngrok
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

    def __init__(self, data, id_mapping=None):
        self.A = data
        self.index = faiss.IndexFlatIP(4499)
        self.index.add(self.A)
        
        
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

alg = np.random.randint(low=0, high=1000, size =(1000, 4499))
Algorithm(alg).run()
