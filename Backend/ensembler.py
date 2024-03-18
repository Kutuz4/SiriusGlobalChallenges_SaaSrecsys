from flask import Flask, request
from flask_ngrok import run_with_ngrok
import json
import requests
from flask import jsonify



app = Flask(__name__)

class Ensembler:
    def __init__(self, a, callable):
        self.a = a
        self.callable = callable
        
    def predict(self, data):   
        predicts = [x.predict(data) for x in self.a]
        return self.callable(predicts)


class connector:
    def __init__(self, url):
        self.url = url 
    def predict(self, user_id):
        data = {'user_id': user_id}
        response = requests.get(f"{self.url}/predict?user_id={user_id}").json()["prediction"]
        return response

connector = connector("https://basilisk-relaxed-ghost.ngrok-free.app/")
ensembler = Ensembler([connector], lambda x: x[0])

@app.route("/")
@app.route('/predict', methods = ['POST', 'GET'])
def answer():
    if request.method == 'POST':
        data = request.post('data')
        prediction = ensembler.predict(data)
        return json.dumps({"prediction": prediction})
    if request.method == 'GET': 
        user_id = request.args.get('user_id')
        config = json.loads(user_id)
        prediction = ensembler.predict(config)
        return json.dumps({"prediction": prediction})
        
           
if __name__ == "__main__":
    app.run()


    


