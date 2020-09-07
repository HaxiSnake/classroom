# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Camera(models.Model):
    classroom_text = models.CharField(max_length=128,verbose_name="教室")
    camera_ip_text = models.CharField(max_length=128,verbose_name="摄像头IP")
    people_number  = models.IntegerField(default=0)
    
    def __str__(self):
        return "<Classroom: {} IP: {}>".format(self.classroom_text,self.camera_ip_text)
            