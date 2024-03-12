from flask import Flask, request

app = Flask(__name__)



class CoreAPI:
    def __init__(self, ensembler,database):
        self.ensembler = ensembler
        self.database = database
    
    def predict_(self, user_id):
        data = self.database[user_id]
        return self.ensembler.predict(data)
    
    def add_user_(self, user_id, data):
        self.database[user_id] = data
    
    def run(self):
        app = Flask(__name__)
        @app.route('/predict', methods=['GET'])
        def predict():
            if request.method == 'GET':
                user_id = request.args['user_id']
                return self.predict_(user_id)
        
        @app.route('/add_user', methods=['POST'] )
        def add_user():
            if request.method == 'POST':
                user_id = request.json["user_id"]
                data = request.json["data"]
                self.add_user_(user_id, data)
                return "200"
            
        app.run(debug=True)


        

