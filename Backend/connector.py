
import json
import requests

class connector:
    def __init__(self, url):
        self.url = url 
    def predict(self, user_id):
        data = {'user_id': user_id}
        response = requests.get(f"{self.url}/predict?user_id={user_id}", data=data)
        return response




# connector1 = connector("http://127.0.0.1:5000")
# user_id = 12345
# response1 = connector1.predict(user_id)
# print(response1)

