import cv2
from PIL import Image
from threading import *

class Camera:
      def __init__(self, url):
          self.con_url = str(url) + "/video"
          self.frame = None
          self.stop_event = Event()
          self.frame_prop = {
              'height': 608,
              'width': 608
          }
          self.cam_thread = None
          self.thread_lock = Lock()
          try:
              self.cap = cv2.VideoCapture(self.con_url)
              if self.cap is None:
                  raise ConnectionError("Connection Error")
              res, frame = self.cap.read()
              if not res:
                  raise ConnectionError("Connection Error")
              self.thread_lock.acquire()
              self.frame = cv2.resize(frame, (int(self.frame_prop['width']), int(self.frame_prop['height'])))
              self.thread_lock.release()
              self.cam_thread = Thread(target=self.__process, daemon=True)
          except (cv2.error, ConnectionError, ThreadError):
              raise Exception("Initialization Error")

      def __process(self):
          try:
              while True:
                  res, frame = self.cap.read()
                  if not res:
                      raise ConnectionError("Connection Error")
                  self.thread_lock.acquire()
                  self.frame = frame
                  self.thread_lock.release()
                  if self.stop_event.is_set():
                      break
          except ConnectionError as e:
             raise ConnectionError(e)

      def cam_start(self):
          self.cam_thread.start()

      def is_running(self):
          return self.cam_thread is not None and self.cam_thread.isAlive()

      def stop(self):
          if self.is_running():
              self.stop_event.set()
              self.cam_thread.join()

      def start(self):
          if self.stop_event.is_set() and not self.is_running():
              self.stop_event.clear()
              self.cam_thread = Thread(target=self.__process, daemon=True)
              self.cam_thread.start()
          else:
              raise Exception("System Error")

      def test(self):
          try:
              res, frame = self.cap.read()
              return self.cap.isOpened() and res
          except (cv2.error, Exception):
              raise ConnectionError("Connection Error")

      def getFrame(self):
          self.thread_lock.acquire()
          frame = self.frame
          self.thread_lock.release()
          return cv2.resize(frame, (int(self.frame_prop['width']), int(self.frame_prop['height'])))

      def getImage(self, img_prop):
          try:
              frame = self.getFrame()
              frame = cv2.resize(frame, (int(img_prop['width']), int(img_prop['height'])))
              cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
              return Image.fromarray(cv2image)
          except cv2.error:
              raise Exception("System Error")

      def __del__(self):
          self.stop()
          self.cap.release()








