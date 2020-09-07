from django.contrib import admin

from .models import Camera
# Register your models here.

class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'classroom_text', 'camera_ip_text','people_number')
    search_fields = ('classroom_text','camera_ip_text')
    fieldsets = (
        (None, {
            'fields': ( 'classroom_text', 'camera_ip_text'),
        }
        ),
    )

admin.site.register(Camera, CameraAdmin)