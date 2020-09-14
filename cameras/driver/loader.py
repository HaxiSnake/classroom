'''
The code is referenced from https://github.com/miguelgrinberg/flask-video-streaming, I did some modify to the code.
'''
import os
import cv2
import time

from django.conf import settings

from .base_camera import BaseCamera



class Loader(BaseCamera):
    

    def __init__(self,video_source):
        self.video_source = video_source
        path = os.path.join(settings.BASE_DIR, "static/cameras/nocapture.png")
        self.default_img = cv2.imread(path)
        self.start_time = time.time()
        super(Loader, self).__init__(video_source)

    def frames(self):
        camera = cv2.VideoCapture(self.video_source)
        if not camera.isOpened():
            # raise RuntimeError('Could not start camera.')
            print("Could not start camera:",self.video_source)
	
        while True:
            # read current frame
            ret, img = camera.read()

            # encode as a jpeg image and return it
            # yield cv2.imencode('.jpg', img)[1].tobytes()
            if ret:
                yield img
            else:
                now = time.time()
                if now - self.start_time > 60:
                    self.start_time = now
                    camera = cv2.VideoCapture(self.video_source)
                yield self.default_img
