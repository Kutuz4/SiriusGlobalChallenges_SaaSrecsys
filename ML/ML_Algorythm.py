import numpy as np
import pandas as pd
from tqdm import tqdm
from rectools.models import PureSVDModel
from rectools import Columns
from rectools.dataset.dataset import Dataset
import pandas as pd
from flask import Flask, request
import json

class Algorithm:

    def __init__(self, data, id_mapping=None):
        self.A = pd.DataFrame(data, columns=[Columns.User, Columns.Item, Columns.Weight, Columns.Datetime])
        self.dataset = Dataset.construct(self.A)

        self.model = PureSVDModel()
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
                user_id = int(request.args['user_id'])
                return json.dumps({"prediction": self.predict_(user_id)})

        app.run(port = 24567)