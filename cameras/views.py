import re
import time 
import io

import mimetypes
from PIL import Image
import cv2
import numpy as np

from django.views import generic, View
from django.http import StreamingHttpResponse,HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.

from .models import Camera
from .driver.loader import Loader
from .utils import tools
from .net.ssd_wrapper import SSD
config_file = "./cameras/net/configs/vgg_ssd512_coco_trainval35k.yaml"
dataset_type = "coco"
weight = "./cameras/net/model/vgg_ssd512_coco_trainval35k.pth"
score_threshold=0.15
ssd = SSD(config_file,dataset_type,weight,score_threshold)
# loader = Loader("/share/dong/class_test/03.mp4")
# img = loader.get_frame()
# print("test start predict")
# tmp = time.time()
# img = ssd.predict(img)
# print("test end predict")
# print(time.time()-tmp)
class IndexView(generic.ListView):
    template_name = 'cameras/index.html'
    context_object_name = "cameras_list"

    def get_queryset(self):
        return Camera.objects.all()

class ClassroomListView(generic.ListView):
    template_name = 'cameras/classroomlist.html'
    context_object_name = "cameras_list"

    def get_queryset(self):
        return Camera.objects.all()

class DetailView(generic.DetailView):
    model = Camera
    template_name = "cameras/detail.html"

def screenshot(request,camera_id):
    camera = get_object_or_404(Camera, pk=camera_id)
    loader = Loader(camera.camera_ip_text)
    img = loader.get_frame()  
    if img is None:
        img = cv2.imread("./static/cameras/nocapture.png")  
    img = ssd.predict(img)
    img = cv2.resize(img,(0,0),fx=0.375,fy=0.375)
    content = tools.img_to_str(img)
    return HttpResponse(content,content_type="image/png")

    

def player(request,camera_id):
    camera = get_object_or_404(Camera, pk=camera_id)
    loader = Loader(camera.camera_ip_text)
    # loader = TestLoader()
    return StreamingHttpResponse(gen(loader), 
                                content_type="multipart/x-mixed-replace; boundary=frame")

def gen(loader):
    while True:
        img = loader.get_frame() 
        if img is None:
            img = cv2.imread("./static/cameras/nocapture.png")  
        else:
            img = ssd.predict(img)
        # bytes_image = Image.fromarray(img).tobytes()
        img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
        frame = tools.img_to_str(img)
        yield (
            b'--frame\r\n'
            b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n'
        )

class TestLoader():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = [open(f+'.jpg','rb').read() for f in ['2','3','4']]

    def pop(self):
        time.sleep(1)
        return self.frames[int(time.time())%3]





    

