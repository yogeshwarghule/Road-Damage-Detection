import tkinter as tk
from Windows.login import LoginPage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("RDD : Road Damage Detector")

    # full screen mode
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(str(screen_width) + "x" + str(screen_height))
    root.resizable(False, False)

    # login page
    LoginPage(root)

    root.mainloop()

