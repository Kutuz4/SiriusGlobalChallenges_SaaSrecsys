import pandas as pd
import numpy as np
from flask import Flask, request
import json
from rectools.models import LightFMWrapperModel
from lightfm import LightFM
from rectools import Columns
from rectools.dataset.dataset import Dataset
from tqdm import tqdm 



data = []
 
with open("/home/arina/combined_data_1.txt", "r") as f: 
    lines = f.readlines() 
movie_id = -1 
for x in tqdm(lines): 
    if "," not in x: 
         movie_id = int(x.strip(":\n")) 
    else: 
        user_id, rating, date = x.split(",") 
        if int(user_id) < 1000000: 
            data.append((movie_id, int(user_id), int(rating), date))



class Algorithm:
    

    def __init__(self,dataset, id_mapping=None):
        self.pd1 = pd.DataFrame(data[::100], columns=[Columns.User, Columns.Item, Columns.Weight, Columns.Datetime])
        self.dataset = Dataset.construct(self.pd1)
        self.model = LightFMWrapperModel(
        model=LightFM(no_components = 30)
        )
        self.model.fit(self.dataset)
        
               
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
        @app.route("/")   
        @app.route('/predict', methods=['GET'])   
        def predict_n(): 
            if request.method == 'GET':
                user_id=int(request.args['user_id'])
                return json.dumps({"prediction": self.predict_(user_id)})
        app.run()

alg = np.random.randint(low=0, high=1000, size =(1000, 4499))
Algorithm(alg).run()
