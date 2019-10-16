import cv2
class Queue():
    def __init__(self,size=100):
        if size<=0 or not isinstance(size,int):
            print("size shoud be larger than 0, set size to default 100")
            size=100
        self.size=size
        self.buff=[]
    def push(self,item):
        if self.isFull():
            return False
        else:
            self.buff.append(item)
            return True
    def pop(self):
        if self.isEmpty():
            return None
        else:
            return self.buff.pop(0)
    def isEmpty(self):
        return len(self.buff)==0
    def isFull(self):
        return len(self.buff)>=self.size
        
class CameraLoaderFactory():
    def __init__(self):
        self.camera_hash={}
    def getCameraLoader(self,camera_name):
        if camera_name not in self.camera_hash:
            self.camera_hash[camera_name]=CameraLoader(camera_name)
        return  self.camera_hash[camera_name]
class CameraLoader():
    def __init__(self,camera_name,buff_size=3):
        self.queue = Queue(buff_size)
        self.camera_name = camera_name
        self.cap = self._get_camera(camera_name)
        self._get_capture_info()
    def _get_camera(self,camera_name):
        cap = cv2.VideoCapture(camera_name)
        ret,frame = cap.read()
        if ret:
            return cap
        else:
            cap.release()
            return None
    def _get_capture_info(self):
        if self.cap:
            self.shape=(int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        else:
            self.shape = (0,0)
            self.fps = 0
    def pop(self):
        while not self.queue.isFull():
            if self.cap:
                ret,frame = self.cap.read()
                if ret:
                    self.queue.push(frame)
                else:
                    break
            else:
                break
        if self.queue.isEmpty():
            return None
        else:
            return self.queue.pop() 
    def release(self):
        self.cap.release()

    