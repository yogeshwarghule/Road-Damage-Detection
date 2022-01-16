import tkinter as tk
from PIL import ImageTk, Image
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
        self.var_authority.set(self.options_authority[0])
        self.drop_authority = tk.OptionMenu(self.top_frame, self.var_authority, *self.options_authority)
        self.drop_authority.config(width=15, font=font)
        self.drop_authority.place(x= int(width_col*2 - 50), y= int(height_row*1))

        self.var_roadcode = tk.StringVar(self.top_frame)
        self.label_roadcode = tk.Label(self.top_frame, text="Road Code :", font=font, padx=5, pady=5)
        self.label_roadcode.place(x= int(width_col*1), y= int(height_row*2))
        self.entry_roadcode = tk.Entry(self.top_frame, width=10, font=font, textvariable=self.var_roadcode)
        self.entry_roadcode.place(x= int(width_col*2 - 50), y= int(height_row*2))

        self.label_time = tk.Label(self.top_frame, text="Time :", font=time_font, pady=5)
        self.label_time.place(x= int(width_col*3 - 10), y= int(height_row*0))
        self.time = tk.Label(self.top_frame, text="12:00", font=time_font, pady=5)
        self.time.place(x = int(width_col*3 + (width_col / 4)*1 - 15)  , y = int(height_row*0))

        self.label_date = tk.Label(self.top_frame, text="Date :", font=time_font, pady=5)
        self.label_date.place(x=int(width_col * 3 + (width_col / 4)*2 - 20), y=int(height_row * 0))
        self.date = tk.Label(self.top_frame, text="03/12/2021", font=time_font, pady=5)
        self.date.place(x=int(width_col * 3 + (width_col / 4) * 3 - 29), y=int(height_row * 0))

        self.label_admin_name = tk.Label(self.top_frame, text="RDD_Admin: " + admin['f_name'] + " " + admin['l_name'], font=time_font, pady=5)
        self.label_admin_name.place(x=int(width_col * 3 + (width_col / 4) * 0 - 10), y=int(height_row * 0 + (height_row / 2) * 1))

        # configure bottom screen
        self.bottom_frame_title = tk.Label(self.bottom_frame, text="Configure System:", font=font, padx=5, pady=5)
        self.bottom_frame_title.place(x= int(width_col*0), y= int(height_row*0))

        self.var_iplink = tk.StringVar(self.bottom_frame)
        self.label_iplink = tk.Label(self.bottom_frame, text="Connection Url :", font=font, padx=5, pady=5)
        self.label_iplink.place(x=int(width_col * 1), y=int(height_row * 1))
        self.entry_iplink = tk.Entry(self.bottom_frame, width=30, font=font, textvariable=self.var_iplink)
        self.entry_iplink.place(x=int(width_col * 2 - 50), y=int(height_row * 1))

        self.button_test = tk.Button(self.bottom_frame, text="Test", command=self.test, font=time_font)
        self.button_test.place(x=int(width_col * 3 + 50), y=int(height_row * 1))

        self.label_gps = tk.Label(self.bottom_frame, text="Camera : ", font=font, padx=5, pady=5)
        self.label_gps.place(x=int(width_col * 1 + (width_col / 2 ) * 0), y=int(height_row * 2))
        self.label_cam_test = tk.Label(self.bottom_frame, text="[OK]", font=font, padx=5, pady=5)
        self.label_cam_test.place(x=int(width_col * 1 + (width_col / 2 ) * 1), y=int(height_row * 2))

        self.label_cam = tk.Label(self.bottom_frame, text="GPS : ", font=font, padx=5, pady=5)
        self.label_cam.place(x=int(width_col * 2), y=int(height_row * 2))
        self.label_cam_test = tk.Label(self.bottom_frame, text="[Error: Unavailable]", font=font, padx=5, pady=5)
        self.label_cam_test.place(x=int(width_col * 2 + (width_col / 2 ) * 1), y=int(height_row * 2))

        self.button_start = tk.Button(self.bottom_frame, text="Start", command=self.start, font=font)
        self.button_start.place(x=int(width_col * 2), y=int(height_row * 3))

    def test(self):
        print("Test")

    def start(self):
        print("Start")