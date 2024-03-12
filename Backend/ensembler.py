from flask import Flask, request
import json
import requests


app = Flask(__name__)

class pr:
    def __init__(self, ban):
        self.ban = ban
    def predict(self, x):
        return [123]


class Ensembler:
    def __init__(self, a, callable):
        self.a = a
        self.callable = callable
        
    def predict(self, data):   
        predicts = [x.predict(data) for x in self.a]
        return self.callable(predicts)
        

ensembler = Ensembler([pr(123)], lambda x: 1)


@app.route('/predict', methods = ['POST', 'GET'])
def answer():
    if request.method == 'POST':
        data = request.json.post('data')
        prediction = ensembler.predict(data)
        print(1, prediction)
        return json.dumps({"prediction": prediction})
    if request.method == 'GET':
        user_id = request.args.get('user-id')
        prediction = ensembler.predict(user_id)
        return json.dumps({"prediction": prediction})
           
if __name__ == "__main__":
    app.run(debug=True)



    


    


