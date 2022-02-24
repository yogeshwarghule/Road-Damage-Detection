import os
from datetime import datetime
import csv
import json
class Record:
    def __init__(self, admin, survey):
        self.dir = './Survey Data'
        self.mkdir()
        self.filepath = self.mkfile()
        # save initial data
        with open(self.filepath, 'a') as file:
            writer = csv.writer(file)
            admin_data = [admin[key] for key in admin]
            survey_data = [survey[key] for key in survey]
            writer.writerow(admin_data)
            writer.writerow(survey_data)
            timedate = [datetime.now().strftime('%d-%m-%Y'), datetime.now().strftime('%H:%M:%S')]
            writer.writerow(timedate)
            with open("./Model/obj.names", "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
            header = ['latitude','longitude']
            for x in self.classes:
                header.append(x)
            writer.writerow(header)
            file.close()
    def add_Damage(self, loc, damage):
        with open(self.filepath, 'a') as file:
            writer = csv.writer(file)
            row = [loc['lat'], loc['long']]
            for types in self.classes:
                row.append(damage.count(types))
            writer.writerow(row)
            file.close()

    def mkdir(self):
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)

    def mkfile(self):
        name = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        path = self.dir + "\\" + name + ".csv"
        with open(path, 'x') as fp:
            pass
        return path

