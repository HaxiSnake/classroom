'''
The code is referenced from https://github.com/miguelgrinberg/flask-video-streaming, I did some modify to the code.
'''
import os
import cv2
from .base_camera import BaseCamera


class Loader(BaseCamera):
    

    def __init__(self,video_source):
        self.video_source = video_source
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
                yield None
