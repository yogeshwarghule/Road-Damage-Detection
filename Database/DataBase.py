import pymysql
import pymysql.cursors

class DataBase():
    host = 'localhost'
    user = 'root'
    password = '1/0=Infinity'
    def __init__(self):
        try:
            self.connection = pymysql.connect(host=self.host, user=self.user,
                                     password=self.password, database='rdd',
                                     cursorclass=pymysql.cursors.DictCursor)
        except: raise ConnectionError('Connection Error')

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
        finally:
            self.connection.close()






