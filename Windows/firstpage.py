import time
import tkinter as tk
from PIL import ImageTk, Image
from threading import *
import datetime

from Sensor.camera import Camera
from Sensor.gps import Gps

from Windows.secondpage import SecondPage
class FirstPage():
    def __init__(self, root, admin):
        self.root = root
        screen_width = root.winfo_screenwidth()//2
        screen_height = root.winfo_screenheight()//2

        width_col = screen_width // 4
        height_row = (screen_height * 0.5) // 4

        font = ("Calibry", 12, "bold")
        time_font = ("Calibary", 10, "bold")
        self.top_frame = tk.Frame(root, height=screen_height * 0.5, width=screen_width * 1.0)
        self.top_frame.pack()


        self.bottom_frame = tk.Frame(root, height=screen_height * 0.5, width=screen_width * 1.0)
        self.bottom_frame.pack()

        # configure top screen
        self.top_frame_title = tk.Label(self.top_frame, text="Survey Details :", font=font, padx=5, pady=5)
        self.top_frame_title.place(x= int(width_col*0), y= int(height_row*0))

        self.label_authority = tk.Label(self.top_frame, text="Authority :", font=font, padx=5, pady=5)
        self.label_authority.place(x= int(width_col*1), y= int(height_row*1))

        self.options_authority =[
            'National Highway',
            'State Highway',
            'District Highway',
            'Rural Road',
            'Urban Road',
            'Project Road'
        ]
        self.var_authority = tk.StringVar(self.top_frame)
        self.var_authority.set('')
        self.drop_authority = tk.OptionMenu(self.top_frame, self.var_authority, *self.options_authority)
        self.drop_authority.config(width=15, font=font, highlightthickness=2)
        self.drop_authority.place(x= int(width_col*2 - 50), y= int(height_row*1))

        self.var_roadcode = tk.StringVar(self.top_frame)
        self.var_roadcode.set('')
        self.label_roadcode = tk.Label(self.top_frame, text="Road Code :", font=font, padx=5, pady=5)
        self.label_roadcode.place(x= int(width_col*1), y= int(height_row*2))
        self.entry_roadcode = tk.Entry(self.top_frame, width=10, font=font, textvariable=self.var_roadcode, highlightthickness=2)
        self.entry_roadcode.place(x= int(width_col*2 - 50), y= int(height_row*2))

        self.var_time = tk.StringVar(self.top_frame)
        self.var_date = tk.StringVar(self.top_frame)
        self.var_time.set("12:30")
        self.var_date.set("3/12/2000")
        self.label_time = tk.Label(self.top_frame, text="Time :", font=time_font, pady=5)
        self.label_time.place(x= int(width_col*3 - 10), y= int(height_row*0))
        self.time = tk.Label(self.top_frame, text=self.var_time.get(), font=time_font, pady=5)
        self.time.place(x = int(width_col*3 + (width_col / 4)*1 - 15)  , y = int(height_row*0))
        self.label_date = tk.Label(self.top_frame, text="Date :", font=time_font, pady=5)
        self.label_date.place(x=int(width_col * 3 + (width_col / 4)*2 - 20), y=int(height_row * 0))
        self.date = tk.Label(self.top_frame, text=self.var_date.get(), font=time_font, pady=5)
        self.date.place(x=int(width_col * 3 + (width_col / 4) * 3 - 29), y=int(height_row * 0))
        # callback
        self.datetime()


        self.label_admin_name = tk.Label(self.top_frame, text="RDD_Admin: " + admin['f_name'] + " " + admin['l_name'], font=time_font, pady=5)
        self.label_admin_name.place(x=int(width_col * 3 + (width_col / 4) * 0 - 10), y=int(height_row * 0 + (height_row / 2) * 1))

        # configure bottom screen
        self.bottom_frame_title = tk.Label(self.bottom_frame, text="Configure System:", font=font, padx=5, pady=5)
        self.bottom_frame_title.place(x= int(width_col*0), y= int(height_row*0))

        self.var_iplink = tk.StringVar(self.bottom_frame)
        self.label_iplink = tk.Label(self.bottom_frame, text="Connection Url :", font=font, padx=5, pady=5)
        self.label_iplink.place(x=int(width_col * 1), y=int(height_row * 1))
        self.entry_iplink = tk.Entry(self.bottom_frame, width=30, font=font, textvariable=self.var_iplink, highlightthickness=2)
        self.entry_iplink.place(x=int(width_col * 2 - 50), y=int(height_row * 1))

        # sensor data
        self.sensor_data = {
            'camera' : 'Invalid',
            'gps':'Invalid'
        }
        self.button_test = tk.Button(self.bottom_frame, text="Test", command=self.test, font=time_font)
        self.button_test.place(x=int(width_col * 3 + 50), y=int(height_row * 1))
        # Multithreading
        self.thread_test = None

        self.label_cam = tk.Label(self.bottom_frame, text="Camera : ", font=font, padx=5, pady=5)
        self.label_cam.place(x=int(width_col * 1 + (width_col / 2 ) * 0), y=int(height_row * 2))
        self.label_cam_test = tk.Label(self.bottom_frame, text="[Test : NAN]", font=font, padx=5, pady=5, fg='gold')
        self.label_cam_test.place(x=int(width_col * 1 + (width_col / 2 ) * 1 - 20), y=int(height_row * 2))

        self.label_gps = tk.Label(self.bottom_frame, text="GPS : ", font=font, padx=5, pady=5)
        self.label_gps.place(x=int(width_col * 2), y=int(height_row * 2))
        self.label_gps_test = tk.Label(self.bottom_frame, text="[Test : NAN]", font=font, padx=5, pady=5, fg='gold')
        self.label_gps_test.place(x=int(width_col * 2 + (width_col / 2 ) * 1 - 45), y=int(height_row * 2))

        self.label_error = tk.Label(self.bottom_frame, text="", font=time_font, padx=5, pady=5, fg='red')
        self.label_error.place(x=int(width_col * 2) - 50, y = int(height_row * 2 + height_row // 2))

        self.button_start = tk.Button(self.bottom_frame, text="Start", command=self.start, font=font)
        self.button_start.place(x=int(width_col * 2), y=int(height_row * 3))

    def datetime(self):
        curr = datetime.datetime.now()
        self.var_date.set(curr.date())
        self.var_time.set(curr.time().strftime("%H:%M"))
        self.time.config(text = self.var_time.get())
        self.date.config(text = self.var_date.get())
        self.top_frame.after(1000, self.datetime)

    def process_test(self):
        self.button_test['state'] = tk.DISABLED
        self.button_start['state'] = tk.DISABLED

        if self.var_iplink.get() == '':
            self.entry_iplink.config(highlightbackground = "red", highlightcolor= "red")
            self.button_test['state'] = tk.NORMAL
            self.button_start['state'] = tk.NORMAL
            self.thread_test = None
            return
        self.label_error.config(text="sensor connections : [wait]", fg='gold')
        self.label_cam_test.config(text="[Test : Wait]", fg='gold')
        self.label_gps_test.config(text="[Test : Wait]", fg='gold')
        self.entry_iplink.config(highlightbackground="black", highlightcolor="black")
        ip_url = "http://" + self.var_iplink.get()
        try:
            self.cam = Camera(ip_url)
            if self.cam.test() == True:
                self.label_cam_test.config(text="[Test : Ok]", fg='green')
                self.sensor_data['camera'] = 'ok'
            else:
                self.label_cam_test.config(text="[Test : Fail]", fg='red')
                self.sensor_data['camera'] = 'fail'
        except Exception as e:
            self.label_cam_test.config(text="[Test : Fail]", fg='red')
            self.sensor_data['camera'] = 'fail'

        try:
            self.gps = Gps(ip_url)
            if self.gps.test() == True:
                self.label_gps_test.config(text="[Test : Ok]", fg='green')
                self.sensor_data['gps'] = 'ok'
            else:
                self.label_gps_test.config(text="[Test : Fail]", fg='red')
                self.sensor_data['gps'] = 'fail'
        except Exception as e:
            self.label_gps_test.config(text="[Test : Fail]", fg='red')
            self.sensor_data['gps'] = 'fail'
        # configure error message
        if self.sensor_data['camera'] == 'ok' and self.sensor_data['gps'] == 'ok':
            self.label_error.config(text="sensor connections : [Ok]", fg='green')
        else:
            self.label_error.config(text="sensor connections : [Fail]", fg='red')

        # release the buttons
        self.button_test['state'] = tk.NORMAL
        self.button_start['state'] = tk.NORMAL


    def test(self):
        self.thread_test = Thread(target=self.process_test)
        self.thread_test.start()

    def start(self):
        # reset error state
        self.label_error.config(text="")
        # validate data
        if self.var_authority.get() == '' or self.entry_roadcode.get() == '':
            if self.var_authority.get() == '':
                self.drop_authority.config(highlightbackground="red", highlightcolor="red")
                self.label_error.config(text="Highlighted Entry : [required]", fg='red')
            else:
                self.drop_authority.config(highlightbackground="black", highlightcolor="black")
            if self.entry_roadcode.get() == '':
                self.entry_roadcode.config(highlightbackground="red", highlightcolor="red")
                self.label_error.config(text="Highlighted Entry : [required]", fg='red')
            else:
                self.entry_roadcode.config(highlightbackground="black", highlightcolor="black")
            return
        else:
            self.drop_authority.config(highlightbackground="black", highlightcolor="black")
            self.entry_roadcode.config(highlightbackground="black", highlightcolor="black")

        # main thread waits until the test thread finish
        if self.thread_test == None:
            self.label_error.config(text="sensor connections : [Invalid]")
            return
        else:
            self.thread_test.join()

        # test for the sensor data
        if not (self.sensor_data['camera'] == 'ok' and self.sensor_data['gps'] == 'ok'):
            self.label_error.config(text="sensor connections : [required]", fg='red')
            return
        # load next second page
        self.top_frame.destroy()
        self.bottom_frame.destroy()
        SecondPage(self.root)










