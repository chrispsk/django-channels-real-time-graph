import websocket
import random
import time
import json
# pip install websocket-client

ws = websocket.WebSocket()
ws.connect('ws://127.0.0.1:8000/ws/some_url/')

for i in range(30):
    time.sleep(1)
    ws.send(json.dumps({'message': i}))