'''
Этот файл будет содержать логику для подключения через WebSocket к серверу,
что используется для реального времени.
Например, когда приходит обновление изображения, клиент будет получать их через WebSocket.
'''

import asyncio
# import websockets
import json

class WSClient:
    def __init__(self, url):
        self.url = url

    # async def connect(self):
    #     async with websockets.connect(self.url) as socket:
    #         await websocket.send(json.dumps({"type": "join", "room": "room1", "user": "alice"}))
    #         response = await websocket.recv()
    #         print(response)
