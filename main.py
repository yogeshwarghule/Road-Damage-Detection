import tkinter as tk    
from Windows.firstpage import FirstPage      
from Windows.login import LoginPage        
from Sensor.camera import Camera    
from Sensor.gps import Gps  
from Windows.secondpage import SecondPage      
if __name__ == "__main__":  
    root = tk.Tk()
    root.title("RDD : Road Damage Detector")    

    # screen size
    screen_width = root.winfo_screenwidth()//2
    screen_height = root.winfo_screenheight()//2
    root.geometry(str(screen_width) + "x" + str(screen_height))  
    root.resizable(False, False)

    # login page
    LoginPage(root)
    # admin = {'id':'3f7f880b-72f5-11ec-98f0-08979872a09a', 'f_name': 'Sameer', 'l_name':'Arote', 'email': 'smrarote@gmail.com'}
    # FirstPage(root, admin)

    # survey_data = {
    #     'authority': "National Highways",
    #     'roadcode': "NH10"
    # }
    # url = "http://192.168.43.1:8080"
    # cam = Camera(url)
    # gps = Gps(url)
    # SecondPage(root, admin, cam, gps, url, survey_data)

    root.mainloop()

