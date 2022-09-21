from django.contrib import admin
from .models import Video

# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'created_at', 'video_file',)    
    list_display = ('title', 'description', 'created_at', 'video_file',)
   
admin.site.register(Video, VideoAdmin)
