import time
import tkinter as tk

import cv2
from PIL import ImageTk, Image
from threading import *
from Database.DataBase import DataBase
from threading import *
import datetime
from Sensor.camera import Camera
from Sensor.gps import Gps

class SecondPage():
    def __init__(self, root, admin, cam, gps, ip_url, survey_data):
       self.root = root
       self.admin = admin
       self.cam = cam
       self.gps = gps
       self.ip_url = ip_url
       self.survey_data = survey_data
       screen_width = (root.winfo_screenwidth() // 4) * 3
       self.img_prop = {
          'width': 720,
          'height': 480
       }
       screen_height = int(self.img_prop['height'])

       self.root.geometry(str(screen_width) + "x" + str(screen_height))
       self.root.resizable(False, False)

       self.cam_frame = tk.Frame(self.root, height=int(self.img_prop['height']), width=self.img_prop['width'], bg='black')
       self.cam_frame.place(x=0, y=0)
       self.cam_feed = tk.Label(self.cam_frame)
       self.cam_feed.place(x=0, y=0)
       self.cam.cam_start()
       self.gps.gps_start()
       self.update()


    def update(self):
       img = self.cam.getImage(self.img_prop)
       imgtk = ImageTk.PhotoImage(image=img)
       self.cam_feed.imgtk = imgtk
       self.cam_feed.configure(image=imgtk)
       print(self.gps.getLocation())
       self.cam_frame.after(100, self.update)














