import requests
import json
import time

with open('config.json') as f:
    data = json.load(f)
t = time.time()
r = requests.post('http://127.0.0.1:8080/api/', json=data)
print(r.json())
