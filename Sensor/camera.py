import time
import cv2
from PIL import Image
from threading import *
import numpy as np
import urllib.request

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
          self.fps = 30
          self.stream_data = b''
          try:
              self.stream = urllib.request.urlopen(self.con_url)
              self.frame = self.readFrame()
          except Exception:
              raise SystemError("Initialization Error")
          self.cam_thread = Thread(target=self.__process, daemon=True)
      def __process(self):
          try:
              while True:
                  self.thread_lock.acquire()
                  self.frame = self.readFrame()
                  self.thread_lock.release()
                  if self.stop_event.is_set():
                      break
                  time.sleep(1//self.fps)
          except ConnectionError as e:
             self.stop()

      def cam_start(self):
          self.stream_data = b''
          self.cam_thread.start()

      def is_running(self):
          return self.cam_thread is not None and self.cam_thread.isAlive()

      def stop(self):
          if self.is_running():
              self.stop_event.set()
              self.cam_thread.join()

      def start(self):
          self.stream_data = b''
          if self.stop_event.is_set() and not self.is_running():
              self.stop_event.clear()
              self.cam_thread = Thread(target=self.__process, daemon=True)
              self.cam_thread.start()
          else:
              self.stop()

      def test(self):
          try:
              data = urllib.request.urlopen(self.con_url)
              return self.stream.getcode() == 200 and data is not None
          except Exception:
              return False

      def readFrame(self):
          try:
              frame = None
              while True:
                  self.stream_data += self.stream.read(1024)
                  b = self.stream_data.find(b'\xff\xd9')  # JPEG end
                  if not b == -1:
                      a = self.stream_data.find(b'\xff\xd8')  # JPEG start
                      jpg = self.stream_data[a:b + 2]  # actual image
                      self.stream_data = self.stream_data[b + 2:]  # other informations
                      if jpg is not b'':
                          frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                      if frame is not None:
                          break
              return frame
          except Exception:
              raise ConnectionError("Connection Error")

      def getFrame(self):
          self.thread_lock.acquire()
          frame = self.frame
          self.thread_lock.release()
          return cv2.resize(frame, (int(self.frame_prop['width']), int(self.frame_prop['height'])), cv2.INTER_AREA)

      def getImage(self, img_prop):
          try:
              frame = self.getFrame()
              frame = cv2.resize(frame, (int(img_prop['width']), int(img_prop['height'])), cv2.INTER_AREA)
              cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
              return Image.fromarray(cv2image)
          except cv2.error:
              raise Exception("System Error")

      def __del__(self):
          self.stop()








