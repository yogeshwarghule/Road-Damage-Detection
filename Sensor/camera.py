import cv2
class Camera():
      def __init__(self, url):
          self.con_url = str(url) + "/video"
          try:
              self.cap = cv2.VideoCapture(self.con_url)
              if self.cap == None:
                  raise ConnectionError("Connection Error")
              res, frame = self.cap.read()
              if not res:
                  raise ConnectionError("Connection Error")
          except (cv2.error, ConnectionError):
              raise ConnectionError("Connection Error")
      def test(self):
          try:
              return self.cap.isOpened()
          except (cv2.error, ConnectionError):
              raise ConnectionError("Connection Error")
      def getFrame(self):
          pass
          # ret, frame = self.cap.read()
          # if frame is not None:
          #     return frame
          # else:
          #     return None
      def __del__(self):
          self.cap.release()







