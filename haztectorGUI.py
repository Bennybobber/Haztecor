import cv2

import _thread
import time
import rel

import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://192.168.194.250:5000") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()

asyncio.run(hello())

capture = cv2.VideoCapture("https://10.65.195.238:8080/video")

while(True):
    _, frame = capture.read()
    cv2.imshow('livestream', frame)

    if cv2.waitKey(1) == ord("q"):
        break
capture.release()
cv2.destroyAllWindows()
