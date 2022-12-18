from django.contrib import admin
from .models import Video, Rating
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class VideoResource(resources.ModelResource):
    class Meta:
        model = Video


class VideoAdmin(ImportExportModelAdmin):
    fields = ('title', 'description', 'created_at', 'video_file', 'creator',)    
    list_display = ('title', 'description', 'created_at', 'video_file','creator',)


class RatingAdmin(admin.ModelAdmin):
    fields = ('rating', 'video', 'author',)
    list_display = ('rating', 'video', 'author',)


admin.site.register(Video, VideoAdmin)
admin.site.register(Rating, RatingAdmin)
