import time
import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import ImageTk, Image
from Database.DataBase import DataBase
from Model.model import Model
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
            self.button_config['state'] = tk.NORMAL
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
            self.label_system_status.config(text="[Error]", fg='red')
        if not self.gps.test() or not self.gps.is_running():
            self.label_gps_status.config(text='[Error]', fg='red')
            self.label_system_status.config(text="[Error]", fg='red')

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
        thread_config = Thread(target=self.start_configure, daemon=True)
        thread_config.start()

    def start_configure(self):
        self.stop()
        if self.threads['pre_process'] is not None and self.threads['pre_process'].isAlive():
            self.events['pre_process'].set()
            self.threads['pre_process'].join()
        self.button_config['state'] = tk.DISABLED
        configwin = tk.Toplevel(self.root)
        configwin.title('Configure Sensor Connection')
        def on_closing():
            configwin.destroy()
            self.button_config['state'] = tk.NORMAL
        configwin.protocol("WM_DELETE_WINDOW", on_closing)
        window_width = int((self.root.winfo_screenwidth() // 6)*2)
        window_height = int(self.img_prop['height']) // 4
        x_cordinate = self.root.winfo_screenwidth() // 2
        y_cordinate = self.root.winfo_screenheight() // 2
        configwin.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        configwin.resizable(False, False)
        # place widget for ui
        row = 3
        col = 5
        small_font = ("Calibry", 12, "bold")
        label = tk.Label(configwin, text="Connection Url: ", font=small_font, padx=5, pady=5)
        label.place(x=(window_width // col) * 0, y=(window_height // row) * 0)

        var_iplink = tk.StringVar(configwin)
        var_iplink.set("")
        entry_iplink = tk.Entry(configwin, width=30, font=small_font, textvariable=var_iplink, highlightthickness=2)
        entry_iplink.place(x=(window_width // col) * 1 + 25, y=(window_height // row) * 0)

        cam = tk.Label(configwin, text="Camera : ", font=small_font, padx=5, pady=5)
        cam.place(x=(window_width // col) * 0, y=(window_height // row) * 1)
        cam_status = tk.Label(configwin, text="[NAN]", font=small_font, padx=5, pady=5, fg='gold')
        cam_status.place(x=(window_width // col) * 1, y=(window_height // row) * 1)

        gps = tk.Label(configwin, text="GPS : ", font=small_font, padx=5, pady=5)
        gps.place(x=(window_width // col) * 3, y=(window_height // row) * 1)
        gps_status = tk.Label(configwin, text="[NAN]", font=small_font, padx=5, pady=5, fg='gold')
        gps_status.place(x=(window_width // col) * 4, y=(window_height // row) * 1)

        button_config = tk.Button(configwin, text="Configure", command=lambda: self.refresh(configwin), font=small_font, width=10, height=1)
        button_config.place(x=(window_width // col) * 2, y=(window_height // row) * 2)
        button_config['state'] = tk.DISABLED

        button_test = tk.Button(configwin, text="test",
                                command=lambda: self.configtest(var_iplink, entry_iplink, cam_status, gps_status, button_config
                                                                ,button_test),
                                font=small_font, width=8, height=1)
        button_test.place(x=(window_width // col) * 4, y=(window_height // row) * 0)

    def configtest(self, var_iplink, entry_iplink, cam_status, gps_status, button_config, button_test):
        thread = Thread(target=self.start_configtest, args=(var_iplink, entry_iplink, cam_status, gps_status, button_config
                                                            , button_test), daemon=True)
        thread.start()

    def start_configtest(self, var_iplink, entry_iplink, cam_status, gps_status, button_config, button_test):
        button_config['state'] = tk.DISABLED
        entry_iplink.config(highlightbackground="black", highlightcolor="black")
        if var_iplink.get() is None or var_iplink.get() is "":
            entry_iplink.config(highlightbackground="red", highlightcolor="red")
            cam_status.config(text="[NAN]", fg='gold')
            gps_status.config(text="[NAN]", fg='gold')
            return
        button_test['state'] = tk.DISABLED
        url = "http://" + var_iplink.get()
        cam_status.config(text="[wait]", fg='gold')
        gps_status.config(text="[wait]", fg='gold')
        try:
            cam = Camera(url)
            gps = Gps(url)
            if cam.test():
                cam_status.config(text="[ok]", fg='green')
            else:
                cam_status.config(text="[fail]", fg='red')
            if gps.test():
                gps_status.config(text="[ok]", fg='green')
            else:
                gps_status.config(text="[fail]", fg='red')
            self.cam.stop()
            self.gps.stop()
            self.cam = cam
            self.gps = gps
            button_config['state'] = tk.NORMAL
        except Exception:
            cam_status.config(text="[fail]", fg='red')
            gps_status.config(text="[fail]", fg='red')
        finally:
            button_test['state'] = tk.NORMAL

    def refresh(self, configwin):
        self.initiate()
        configwin.destroy()

    def stop(self):
        thread = Thread(target=self.start_stop, daemon=True)
        thread.start()

    def start_stop(self):
        self.events['thread_read'].set()
        self.events['thread_process'].set()
        self.events['thread_database'].set()
        self.button_stop['state'] = tk.DISABLED
        if self.threads['thread_read'] is not None and self.threads['thread_read'].isAlive():
            self.threads['thread_read'].join()
        if self.threads['thread_process'] is not None and self.threads['thread_process'].isAlive():
            self.threads['thread_process'].join()
        if self.threads['thread_database'] is not None and self.threads['thread_database'].isAlive():
            self.threads['thread_database'].join()

        self.label_system_status.config(text="[Stopped]", fg='red')
        self.button_start['state'] = tk.NORMAL

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
                time.sleep(3)
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
        model = Model()
        try:
            while True:
                data = self.process_queue.get()
                frame, damages, confidences = model.getPrediction(data['frame'])
                # update feed
                frame = cv2.resize(frame, (int(self.img_prop['width']), int(self.img_prop['height'])), cv2.INTER_AREA)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.cam_feed.imgtk = imgtk
                self.cam_feed.configure(image=imgtk)
                self.cam_feed.image = imgtk
                self.process_queue.task_done()
                self.output_queue.put({'location': data['location'], 'damage': damages})
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





















