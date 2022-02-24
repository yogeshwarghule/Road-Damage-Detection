import pymysql
import pymysql.cursors
import pymysql.err
class DataBase:
    host = 'localhost'
    user = 'root'
    password = '1/0=Infinity'
    def __init__(self):
        try:
            self.connection = pymysql.connect(host=self.host, user=self.user,
                                     password=self.password, database='rdd',
                                     cursorclass=pymysql.cursors.DictCursor)
        except: raise ConnectionError('Connection Error')
        with open("./Model/obj.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.survey_id = None

    def login(self, id, password):
        try:
            with self.connection.cursor() as cursor:
              cursor.execute('select id,f_name,l_name,email from admin where id = %s and password = md5(%s)',
                       (id, password))
              data = cursor.fetchone()
              if data == None:
                  return {'error': "Invalid Credentials", 'verified': False}
              else:
                  return {'admin': data, 'verified': True}
        except Exception as e:
             return {'error': "Database Error", 'verified': False}

    def createSurvey(self, admin, survey_data):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO survey (id, rdd_id, authority, roadcode) VALUES (uuid(), %s, %s, %s)",
                              (admin['id'], survey_data['authority'], survey_data['roadcode']))
                self.connection.commit()
                # how to get the last inserted row id
                cursor.execute("SELECT id FROM survey WHERE rdd_id = %s ORDER BY timestamp Desc Limit 1", (admin['id']))
                data = cursor.fetchone()
                self.survey_id = data['id']
        except Exception as e:
            print(e)
            raise ConnectionError(e)

    def addData(self, location, damage):
        query_data = [self.survey_id, location['lat'], location['long']]
        for types in self.classes:
            query_data.append(damage.count(types))
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO data (survey_id, latitude, longitude, D00, D10, D20, D40)"
                               " VALUES (%s, %s, %s, %s, %s, %s, %s)",
                               tuple(query_data))
                self.connection.commit()
        except Exception as e:
            print(e)
            raise ConnectionError(e)

    def __del__(self):
        self.connection.close()
