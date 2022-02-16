import time
import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import ImageTk, Image
from threading import *
from Database.DataBase import DataBase
from threading import *
import datetime
from Sensor.camera import Camera
from Sensor.gps import Gps
import queue

class SecondPage():
    def __init__(self, root, admin, cam, gps, ip_url, survey_data):
       self.root = root
       self.admin = admin
       self.cam = cam
       self.gps = gps
       self.ip_url = ip_url
       self.survey_data = survey_data
       screen_width = (root.winfo_screenwidth() // 6) * 4
       self.img_prop = {
          'width': 720,
          'height': 480
       }
       screen_height = int(self.img_prop['height'])
       row = 8
       self.root.geometry(str(screen_width) + "x" + str(screen_height))
       self.root.resizable(False, False)

       self.cam_frame = tk.Frame(self.root, height=int(self.img_prop['height']), width=self.img_prop['width'], bg='black')
       self.cam_frame.place(x=0, y=0)
       self.cam_feed = tk.Label(self.cam_frame)
       self.cam_feed.pack(expand='YES', fill="both")

       second_screen_width = int(screen_width - int(self.img_prop['width']))
       self.system_frame = tk.Frame(self.root, height=int(self.img_prop['height']), width=second_screen_width)
       self.system_frame.place(x=int(self.img_prop['width']), y=0)
       large_front = ("Calibry", 15, "bold")
       small_font = ("Calibry", 12, "bold")

       self.label_lat = tk.Label(self.system_frame, text="Latitude: 19.2819166", font=large_front, padx=5, pady=5)
       self.label_lat.place(x=0, y=(screen_height//row)*0)
       self.label_long = tk.Label(self.system_frame, text="Longitude: 70.11119191", font=large_front, padx=5, pady=5)
       self.label_long.place(x=0, y=(screen_height // row) * 1)
       self.label_cam = tk.Label(self.system_frame, text="Camera :", font=small_font, padx=5, pady=5)
       self.label_cam.place(x=(second_screen_width // 4)*0, y=(screen_height // row) * 2)
       self.label_cam_status = tk.Label(self.system_frame, text="[ok]", font=small_font, padx=5, pady=5, fg='green')
       self.label_cam_status.place(x=(second_screen_width // 4)*1, y=(screen_height // row) * 2)

       self.label_gps = tk.Label(self.system_frame, text="GPS :", font=small_font, padx=5, pady=5)
       self.label_gps.place(x=(second_screen_width // 4) * 2, y=(screen_height // row) * 2)
       self.label_gps_status = tk.Label(self.system_frame, text="[ok]", font=small_font, padx=5, pady=5, fg='green')
       self.label_gps_status.place(x=(second_screen_width // 4) * 3-25, y=(screen_height // row) * 2)
       self.button_config = tk.Button(self.system_frame, text="configure", command=self.configure, font=small_font,
                                      width=29, height=2)
       self.button_config.place(x=(second_screen_width) // 2 - 150, y=(screen_height // row) * 3)

       self.label_system = tk.Label(self.system_frame, text="RDD Status :", font=large_front, padx=5, pady=5)
       self.label_system.place(x=((second_screen_width // 2) * 0), y=(screen_height // row) * 4)
       self.label_system_status = tk.Label(self.system_frame, text="[Wait]", font=large_front, padx=5, pady=5, fg='gold')
       self.label_system_status.place(x=((second_screen_width // 2) * 1)-25, y=(screen_height // row) * 4)

       self.var_date = tk.StringVar()
       self.var_time = tk.StringVar()
       self.var_date.set("12-12-2022")
       self.var_time.set("12:30:00")
       self.label_time = tk.Label(self.system_frame, text="Time : ", font=small_font, padx=5, pady=5)
       self.label_time.place(x=(second_screen_width // 4) * 0, y=(screen_height // row) * 5)
       self.time = tk.Label(self.system_frame, text=self.var_time.get(), font=small_font, padx=5, pady=5)
       self.time.place(x=(second_screen_width // 4) * 1-25, y=(screen_height // row) * 5)
       self.label_date = tk.Label(self.system_frame, text="Date : ", font=small_font, padx=5, pady=5)
       self.label_date.place(x=(second_screen_width // 4) * 2, y=(screen_height // row) * 5)
       self.date = tk.Label(self.system_frame, text=self.var_date.get(), font=small_font, padx=5, pady=5)
       self.date.place(x=(second_screen_width // 4) * 3-25, y=(screen_height // row) * 5)


       self.button_start = tk.Button(self.system_frame, text="start", command=self.start, font=small_font,
                                     width=29, height=2)
       self.button_start.place(x=(second_screen_width) // 2 - 150, y=(screen_height // row) * 6)
       self.button_stop = tk.Button(self.system_frame, text="stop", command=self.stop, font=small_font,
                                     width=14, height=2)
       self.button_stop.place(x=((second_screen_width // 2) * 0), y=(screen_height // row) * 7)
       self.button_close = tk.Button(self.system_frame, text="close", command=self.close, font=small_font,
                                     width=14, height=2)
       self.button_close.place(x=(second_screen_width//2)*1, y=(screen_height // row) * 7)

       self.threads = {'pre_process': None,
                       'thread_read': None,
                       'thread_process': None,
                       'thread_database': None,
                       'thread_sensor': None
                       }
       self.events = {'pre_process': Event(),
                      'thread_read': Event(),
                      'thread_process': Event(),
                      'thread_database': Event(),
                      }
       self.process_queue = queue.Queue()
       self.output_queue = queue.Queue()
       self.initiate()

    def initiate(self):
        try:
            self.button_stop['state'] = tk.DISABLED
            self.datetime()
            self.cam.cam_start()
            self.gps.gps_start()
            # Thread(target=self.pre_process, daemon=True)
            self.threads['pre_process'] = Thread(target=self.pre_process, daemon=True)
            self.threads['pre_process'].start()
            # self.threads['thread_sensor'] = Thread(target=self.test_sensor, daemon=True)
            # self.threads['thread_sensor'].start()
            self.label_system_status.config(text="[Ready]", fg='green')
        except Exception:
            self.button_start['state'] = tk.DISABLED
            self.label_system_status.config(text="[Error]", fg='red')
            self.test_sensor()

    def test_sensor(self):
        if not self.cam.test() or not self.cam.is_running():
            self.label_cam_status.config(text='[Error]', fg='red')
        if not self.gps.test() or not self.gps.is_running():
            print(self.gps.test())
            print(self.gps.is_running())
            self.label_gps_status.config(text='[Error]', fg='red')


    def pre_process(self):
        self.events['pre_process'].clear()
        try:
            while True:
                if not self.cam.is_running() or not self.gps.is_running():
                    raise ConnectionError("Connection Error")
                img = self.cam.getImage(self.img_prop)
                imgtk = ImageTk.PhotoImage(image=img)
                self.cam_feed.imgtk = imgtk
                self.cam_feed.configure(image=imgtk)
                self.cam_feed.image = imgtk
                loc = self.gps.getLocation()
                self.label_lat.config(text="Latitude: " + str(loc['lat']))
                self.label_long.config(text="Longitude: " + str(loc['long']))
                if self.events['pre_process'].is_set():
                    break
                time.sleep(0.1)
        except ConnectionError:
            self.test_sensor()

    def datetime(self):
       curr = datetime.datetime.now()
       self.var_date.set(curr.date())
       self.var_time.set(curr.time().strftime("%H:%M:%S"))
       self.time.config(text=self.var_time.get())
       self.date.config(text=self.var_date.get())
       self.system_frame.after(1000, self.datetime)

    def configure(self):
       pass

    def stop(self):
        self.events['thread_read'].set()
        self.events['thread_process'].set()
        self.events['thread_database'].set()

        if self.threads['thread_read'] is not None and self.threads['thread_read'].isAlive():
            self.threads['thread_read'].join()
        if self.threads['thread_process'] is not None and self.threads['thread_process'].isAlive():
            self.threads['thread_process'].join()
        if self.threads['thread_database'] is not None and self.threads['thread_database'].isAlive():
            self.threads['thread_database'].join()

        self.label_system_status.config(text="[Stopped]", fg='red')
        self.button_start['state'] = tk.NORMAL
        self.button_stop['state'] = tk.DISABLED

    def start(self):
        self.events['thread_read'].clear()
        self.events['thread_process'].clear()
        self.events['thread_database'].clear()

        # 'pre_process': Thread(target=self.pre_process, daemon=True)
        # 'thread_read': Thread(target=self.read, daemon=True)
        # 'thread_process': Thread(target=self.process, daemon=True)
        # 'thread_database': Thread(target=self.database, daemon=True)

        # Empty the process and output queue

        try:
            while True:
                self.process_queue.get_nowait()
        except queue.Empty:
            pass
        try:
            while True:
                self.output_queue.get_nowait()
        except queue.Empty:
            pass

        self.threads['thread_read'] = Thread(target=self.read, daemon=True)
        self.threads['thread_process'] = Thread(target=self.process, daemon=True)
        self.threads['thread_database'] = Thread(target=self.database, daemon=True)

        self.threads['thread_read'].start()
        self.threads['thread_process'].start()
        self.threads['thread_database'].start()

        self.button_start['state'] = tk.DISABLED
        self.button_stop['state'] = tk.NORMAL
        self.label_system_status.config(text="[Running]", fg='green')

    def close(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit RDD?"):
            self.stop()
            self.root.quit()

    def read(self):
        try:
            while True:
                if not self.cam.is_running() or not self.gps.is_running():
                    raise ConnectionError("Connection Error")
                frame = self.cam.getFrame()
                loc = self.gps.getLocation()
                time.sleep(2)
                self.process_queue.put({'frame': frame, 'location': loc})
                if self.events['thread_read'].is_set():
                    break
        except ConnectionError:
            self.test_sensor()

    def process(self):
        # stop preprocessing
        if self.threads['pre_process'].isAlive():
            self.events['pre_process'].set()
            self.threads['pre_process'].join()
        try:
            while True:
                data = self.process_queue.get()
                print(data)
                time.sleep(1)
                self.process_queue.task_done()
                self.output_queue.put({'location': data['location'], 'damage': 'D10'})
                if self.events['thread_process'].is_set():
                    break
        except ConnectionError:
            self.test_sensor()

    def database(self):
        try:
            while True:
                data = self.output_queue.get()
                print("saving ")
                time.sleep(0.1)
                print(data)
                self.output_queue.task_done()
                if self.events['thread_database'].is_set():
                    break
        except ConnectionError:
            self.test_sensor()





















