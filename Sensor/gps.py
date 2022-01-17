import cv2
import requests as req
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class Gps():
      def __init__(self, url):
          self.con_url = url + '/gps.json'

      def test(self):
          try:
              http_con = req.Session()
              retries = Retry(total=1,
                              backoff_factor=0.1,
                              status_forcelist=[500, 502, 503, 504])
              http_con.mount('http://', HTTPAdapter(max_retries=retries))
              return http_con.get(self.con_url, verify=False).status_code == 200
          except Exception as e:
              raise Exception(e)
      def getData(self):
          pass
          # gps_data = req.get(self.url, verify=False)
          # if gps_data is not None:
          #   return gps_data
          # else:
          #   return None