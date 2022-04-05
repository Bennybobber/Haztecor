from tkinter import *
import tkinter
from threading import Thread
import serial
import cv2
import PIL.Image, PIL.ImageTk
import time
import keyboard
import websockets
import asyncio
import json

class ZumoControl:
    def __init__(self):
        self.ser = serial.Serial("COM16", 9600, timeout=1)
    
    def keyworker(self):
        while True:
            key = keyboard.read_key()
            if key == 's' or key == 'a' or key == 'w' or key == 'd':
                self.ser.write(key.encode())
            elif key !='w'  or  key != 'a' or key != 's' or key != 'd':
                key = ''

class SensorInput:
    def __init__(self):
        self.sensordict = {"cpm": '0', "temp": '0', "light": 'light'}
        self.maxTemp = "0"
        self.lightLevel = "0"
        self.maxCPM = "0"
        self.maxdangerdict = {"cpmText": "Safe", "cpmColour": "green", "tempText": "Safe", "tempColour": "green"}
        self.dangerdict = {"cpmText": "Safe", "cpmColour": "green", "tempText": "Safe", "tempColour": "green"}
    def setDangerLevels(self):
        if int(self.maxCPM) >= 50 and int(self.maxCPM) <= 200:
            self.maxdangerdict["cpmText"] = "Warning"
            self.maxdangerdict["cpmColour"] = "yellow"
        elif int(self.maxCPM) < 50 :
            self.maxdangerdict["cpmText"] = "Safe"
            self.maxdangerdict["cpmColour"] = "green"
        elif int(self.maxCPM) > 200 :
            self.maxdangerdict["cpmText"] = "Danger"
            self.maxdangerdict["cpmColour"] = "red"
        
        if int(self.maxTemp) >= 25 and int(self.maxTemp) <= 39:
            self.maxdangerdict["tempText"] = "Warning"
            self.maxdangerdict["tempColour"] = "yellow"
        elif int(self.maxTemp) > 40 :
            self.maxdangerdict["tempText"] = "Danger"
            self.maxdangerdict["tempColour"] = "red"

        if int(self.sensordict["cpm"]) >= 50 and int(self.sensordict["cpm"]):
            self.dangerdict["cpmText"] = "Warning"
            self.dangerdict["cpmColour"] = "yellow"
        elif int(self.sensordict["cpm"]) < 50 :
            self.dangerdict["cpmText"] = "Safe"
            self.dangerdict["cpmColour"] = "green"
        elif int(self.sensordict["cpm"]) > 200 :
            self.dangerdict["cpmText"] = "Danger"
            self.dangerdict["cpmColour"] = "red"
        
        if int(self.sensordict["temp"]) >= 25 and int(self.sensordict["cpm"]) <= 39:
            self.dangerdict["tempText"] = "Warning"
            self.dangerdict["tempColour"] = "yellow"
        elif int(self.sensordict["temp"]) > 40 :
            self.dangerdict["tempText"] = "Danger"
            self.dangerdict["tempColour"] = "red"
        else:
            self.dangerdict["tempText"] = "Safe"
            self.dangerdict["tempColour"] = "green"

            

    async def values(self, websocket):
        async for message in websocket:
            obj = json.loads(message)
            self.sensordict =  obj
            if int(obj["cpm"]) > int(self.maxCPM):
                self.maxCPM = obj["cpm"]
            if int(obj["temp"]) > int(self.maxTemp):
                self.maxTemp = obj["temp"]
            if int(obj["light"]) >= 80:
                self.sensordict["light"] = "LIGHT"
            else:
                self.sensordict["light"] = "DARK"

            self.setDangerLevels()
            
    async def main(self):
        async with websockets.serve(self.values, "", 5000, ping_interval=None):
            await asyncio.Future()

    def start(self):
        asyncio.run(self.main())

        
        
class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        #start thread to send zumo

        self.zumo = ZumoControl()
        self.zumothread = Thread(target=self.zumo.keyworker)
        self.zumothread.daemon = True
        self.zumothread.start()

        self.sensors = SensorInput()
        self.sensorthread = Thread(target=self.sensors.start)
        self.sensorthread.daemon = True
        self.sensorthread.start()
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
 
         # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
 
        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        
         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
 
        self.window.mainloop()
 
    def snapshot(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()
 
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
 
    def update(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        self.canvas.delete("all")
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            # Add labels
            # print(self.sensors.sensordict)
            tempL =Label(self.canvas,text = "Temperature: " + self.sensors.sensordict["temp"] + " degrees" + " (" + self.sensors.dangerdict["tempText"]+")", bg=self.sensors.dangerdict["tempColour"])
            tempL.place(x = 5, y = 5) 
            cpmL = Label(self.canvas,text = "Counts Per Minute: " + self.sensors.sensordict["cpm"] + " (" + self.sensors.dangerdict["cpmText"]+")", bg=self.sensors.dangerdict["cpmColour"])
            cpmL.place(x = 5, y = 45)
            lightL = Label(self.canvas,text = "Light Level: " + self.sensors.sensordict["light"])
            lightL.place(x = 5, y = 85)
            maxTL = Label(self.canvas,text = "Maximum temperature: " + self.sensors.maxTemp + " (" + self.sensors.maxdangerdict["tempText"]+")", bg=self.sensors.maxdangerdict["tempColour"])
            maxTL.place(x = 5, y = 125)
            maxCPML = Label(self.canvas,text = "Maximum CPM: " + self.sensors.maxCPM + " (" + self.sensors.maxdangerdict["cpmText"]+")", bg=self.sensors.maxdangerdict["cpmColour"])
            maxCPML.place(x = 5, y = 165)    
 
        self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture("https://192.168.194.169:8080/video")
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (ret, None)
 
     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()
 
# Create a window and pass it to the Application object
App(tkinter.Tk(), "Haztector")