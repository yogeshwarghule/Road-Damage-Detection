import requests as req
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from threading import *

class Gps:
      def __init__(self, url):
          self.con_url = url + '/gps.json'
          self.http_con = req.Session()
          retries = Retry(total=1, backoff_factor=0.1,
                               status_forcelist=[500, 502, 503, 504])
          self.http_con.mount('http://', HTTPAdapter(max_retries=retries))
          self.loc = {
                      'lat': '',
                      'long': ''
                  }
          self.thread_gps = Thread(target=self.__process, daemon=True)
          self.stop_event = Event()
          self.thread_lock = Lock()
      def __process(self):
          try:
              while True:
                  location = self.http_con.get(self.con_url, verify=False)
                  if location.status_code == 200:
                      self.thread_lock.acquire()
                      if 'gps' in location.json().keys() and location.json()['gps'] != {} and 'network' in location.json().keys() and location.json()['network'] != {}:
                          if int(location.json()['gps']['accuracy']) > int(location.json()['network']['accuracy']):
                              self.loc['lat'] = location.json()['gps']['latitude']
                              self.loc['long'] = location.json()['gps']['longitude']
                          else:
                              self.loc['lat'] = location.json()['network']['latitude']
                              self.loc['long'] = location.json()['network']['longitude']
                      else:
                          if 'gps' in location.json().keys() and location.json()['gps'] != {}:
                              self.loc['lat'] = location.json()['gps']['latitude']
                              self.loc['long'] = location.json()['gps']['longitude']
                          elif 'network' in location.json().keys() and location.json()['network'] != {}:
                              self.loc['lat'] = location.json()['network']['latitude']
                              self.loc['long'] = location.json()['network']['longitude']
                          else:
                              raise ConnectionError("Connection Error")
                      self.thread_lock.release()
                  else:
                      raise ConnectionError("Connection Error")
                  if self.stop_event.is_set():
                      break
          except ConnectionError as e:
              self.stop()

      def gps_start(self):
          self.thread_gps.start()

      def is_running(self):
          self.thread_gps is not None and self.thread_gps.isAlive()

      def stop(self):
          if self.is_running():
              self.stop_event.set()
              self.thread_gps.join()

      def start(self):
          if self.stop_event.is_set() and not self.is_running():
              self.stop_event.clear()
              self.thread_gps = Thread(target=self.__process, daemon=True)
              self.thread_gps.start()
          else:
              raise Exception("System Error")

      def test(self):
          try:
              return self.http_con.get(self.con_url, verify=False).status_code == 200
          except Exception as e:
              raise ConnectionError("Connection Error")

      def getLocation(self):
          self.thread_lock.acquire()
          loc = self.loc
          self.thread_lock.release()
          return loc

      def __del__(self):
          self.stop()