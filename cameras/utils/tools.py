import cv2
import numpy as np
def img_to_str(img):
    _, buff = cv2.imencode('.png', img)
    return np.array(buff).tostring()