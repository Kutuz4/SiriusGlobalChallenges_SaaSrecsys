
import sqlite3
import numpy as np
import pandas as pd
from tqdm import tqdm
from flask import Flask, request
import csv
import requests
import socket

app = Flask(__name__)

conn = sqlite3.connect("./krut.db")
cursor = conn.cursor()
socket_url = "127.0.0.1"

with open("combined_data_1.txt", "r") as f:
    lines = f.readlines()
    for line in tqdm(lines):
        if ":" in line:
            movie_id = int(line.strip(":\n"))
        else:
            user_id, rating, date = line.split(",")
            if int(user_id) < 1000000:
                datat = (movie_id, user_id, rating, date.strip())
                cursor.execute('INSERT INTO krut_movies (movie_id, user_id, rating, date) VALUES (?, ?, ?, ?);', datat)
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'GET':
        conn = sqlite3.connect("./krut.db")
        cursor = conn.cursor()
        user_id = request.args.get('user_id')
        movie_id = request.args.get('movie_id')
        rating = request.args.get('rating')
        date = request.args.get('date')
        datat = (movie_id, user_id, rating, date)
        cursor.execute('INSERT INTO krut_movies (movie_id, user_id, rating, date) VALUES (?, ?, ?, ?);', datat)
        conn.commit()
        return 'Данные успешно добавлены'

@app.route("/getuser", methods=["GET"])
def getuser():
    user_id = request.args.get('user_id')
    if user_id:
        cursor.execute("SELECT * FROM krut_movies WHERE user_id = ?", (user_id,))
        data = cursor.fetchall()
        return {'data': data}
    return 'Такого пользователя нет'

def send_file(file_name, server_socket):
    with open(file_name, 'rb') as file:
        for data in iter(lambda: file.read(1024), b''):
            server_socket.sendall(data)
            
@app.route("/getdata", methods=["GET"])
def getdata():
    port = requests.args.get("port")
    host = socket_url
    data_to_send = cursor.execute("SELECT * FROM krut_movies")
    data = cursor.fetchall()
    row_count = 0 
    with open("data.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            writer.writerow(row)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    send_file("data.csv", client_socket)
    client_socket.close()
if __name__ == "__main__":
    app.run()

conn.close() 
