

#async def hello():
    #async with websockets.serve("ws://192.168.194.250:5000") as websocket:
        #await websocket.send("Hello world!")
        #await websocket.recv()

#asyncio.run(hello())
import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "", 5000):
        await asyncio.Future()  # run forever

asyncio.run(main())
#capture = cv2.VideoCapture("https://10.65.195.238:8080/video")
#capture = cv2.VideoCapture("https://100.73.3.78:8080/video")

#while(True):
    #_, frame = capture.read()
    #cv2.imshow('livestream', frame)
    #cv2.line(frame,(0,0),(511,511),(255,0,0),5)

    #if cv2.waitKey(1) == ord("q"):
        #break
#capture.release()
#cv2.destroyAllWindows()
