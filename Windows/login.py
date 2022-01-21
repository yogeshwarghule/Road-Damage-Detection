import tkinter as tk
from PIL import ImageTk, Image
from Database.DataBase import DataBase
from Windows.firstpage import FirstPage
class LoginPage :
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()//2
        screen_height = root.winfo_screenheight()//2
        font = ("Calibary", 12, "bold")
        entry_font = ("Calibary", 10, "bold")

        # First Frame
        self.right_frame = tk.Frame(root, height=screen_height * 0.5, width=screen_width * 0.5)
        self.right_frame.grid(row=0, column=1)

        self.left_frame_title = tk.Label(self.right_frame, padx=5, pady=5)
        icon = ImageTk.PhotoImage(Image.open('Public/images/loginicon.png'))
        self.left_frame_title.config(image=icon)
        self.left_frame_title.image = icon
        self.left_frame_title.grid(row=0, column=2)


        self.label_id = tk.Label(self.right_frame, text="RDD_ID :", font=font, padx=5, pady=5)
        self.label_id.grid(row=1, column=1)
        self.entry_id = tk.Entry(self.right_frame, width=36, font=entry_font)
        self.entry_id.grid(row=1, column=2)

        self.label_password = tk.Label(self.right_frame, text="Password:", font=font, padx=5, pady=10)
        self.label_password.grid(row=2, column=1)
        self.entry_password = tk.Entry(self.right_frame, width=36, show="*", font=entry_font)
        self.entry_password.grid(row=2, column=2)

        self.label_error = tk.Label(self.right_frame, text ="", padx = 5, pady=5, fg='red')
        self.label_error.grid(row=3,column=2)

        self.button_login = tk.Button(self.right_frame, text="Login", command=self.login, font=font)
        self.button_login.grid(row=4, column=2)

        # Second Frame
        self.left_frame = tk.Frame(root, height=screen_height * 1, width=screen_width * 0.5, background='red')
        self.left_frame.grid(row=0, column=0)

        img = ImageTk.PhotoImage(
            Image.open('Public/images/login.jpg').resize((int(screen_width * 0.5), int(screen_height * 1)),
                                                         Image.ANTIALIAS))
        left_img = tk.Label(self.left_frame, image=img, height=screen_height * 1, width=screen_width * 0.5)
        left_img.image = img
        left_img.pack()


    def login(self):
        id = self.entry_id.get()
        password = self.entry_password.get()
        if id == '' or password == '':
           self.label_error.config(text = "All feilds are require for login")
        else:
            try:
                db = DataBase()
                res = db.login(id,password)
                if res['verified'] == True:
                    self.left_frame.destroy()
                    self.right_frame.destroy()
                    FirstPage(self.root, res['admin'])
                else:
                    self.label_error.config(text=res['error'])
                    self.entry_password.delete(0, 'end')
                    self.entry_id.delete(0, 'end')
            except Exception as e:
                self.label_error.config(text=e)
                self.entry_password.delete(0, 'end')
                self.entry_id.delete(0, 'end')






