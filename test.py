from cameras.net.ssd_wrapper import SSD
from cameras.driver.loader import Loader
import time
import cv2
config_file = "./cameras/net/configs/vgg_ssd512_coco_trainval35k.yaml"
dataset_type = "coco"
weight = "./cameras/net/model/vgg_ssd512_coco_trainval35k.pth"
score_threshold=0.15
ssd = SSD(config_file,dataset_type,weight,score_threshold)
# loader = Loader("/share/dong/class_test/03.mp4")
cap = cv2.VideoCapture("/share/dong/class_test/03.mp4")
ret, img = cap.read()
# img = cv2.imread("./static/cameras/nocapture.png")
print("test start predict")
tmp = time.time()
img = ssd.predict(img)
print("test end predict")
print(time.time()-tmp)
exit()