from django.contrib import admin
from .models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class VideoResource(resources.ModelResource):

    class Meta:
        model = Video

class VideoAdmin(ImportExportModelAdmin):
    fields = ('title', 'description', 'created_at', 'video_file',)    
    list_display = ('title', 'description', 'created_at', 'video_file',)
 
admin.site.register(Video, VideoAdmin)
