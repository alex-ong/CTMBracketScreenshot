import requests
import json
import time

server_root = "http://127.0.0.1:8080/"
with open('config.json') as f:
    data = json.load(f)
t = time.time()
r = requests.post(server_root+'api/', json=data)

print(r.json())
print("The response took: " + str(time.time() - t) + "seconds")

print("downloading files from server...")
t = time.time()
r = r.json()
if 'files' in r:
    for file in r['files']:
        response = requests.get(server_root+file)
        print(len(response.content))
print("total download took" + str(time.time() - t) + "seconds")
