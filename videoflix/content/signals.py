import os
from django.dispatch import receiver
from .models import Video
from django.db.models.signals import post_save, post_delete
from .tasks import convert480p
import django_rq

"""
Called whenever a video is created or edited.
"""
@receiver(post_save, sender = Video)
def video_post_save(sender, instance, created, **kwargs): 

    if created:
        video_path_as_str = str(instance.video_file)
        modified_video_path = '.' + video_path_as_str[6:]
        queue = django_rq.get_queue('default', autocommit = True)
        queue.enqueue(convert480p, modified_video_path)

"""
Called whenever a video is deleted. It deletes the video file from the videos folder. Without this function video objects could be 
deleted, however the deletion of these would not automatically delete their video files (which are stored in the videos folder, inside 
the media folder).
"""
@receiver(post_delete, sender = Video)
def video_post_delete(sender, instance, **kwargs): 
    
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            video_path_as_str = str(instance.video_file.path)
            same_video_with_480p_format_path = video_path_as_str[:-4] + '_480p.mp4'
            os.remove(same_video_with_480p_format_path)
