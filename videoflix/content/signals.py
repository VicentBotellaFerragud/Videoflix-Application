import os
from django.dispatch import receiver
from .models import Video
from django.db.models.signals import post_save, post_delete
from .tasks import convert_video
import django_rq
import speedtest

"""
Calculates the upload speed.
"""
def calculate_upload_speed():
    
    speed_test = speedtest.Speedtest(secure = True)
    speed_test.get_best_server()
    upload_speed = speed_test.upload() 
    upload_speed_in_mbs = round(upload_speed / (10**6), 2)

    return upload_speed_in_mbs

"""
Called whenever a video is created or edited.
"""
@receiver(post_save, sender = Video)
def video_post_save(sender, instance, created, **kwargs): 

    upload_speed_in_mbs = calculate_upload_speed()

    if upload_speed_in_mbs <= 5:
        queue = django_rq.get_queue('default', autocommit = True)
        queue.enqueue(convert_video, instance.video_file.path, 480)

    elif upload_speed_in_mbs > 5 and upload_speed_in_mbs <= 10:
        queue = django_rq.get_queue('default', autocommit = True)
        queue.enqueue(convert_video, instance.video_file.path, 720)

    elif upload_speed_in_mbs > 10:
        queue = django_rq.get_queue('default', autocommit = True)
        queue.enqueue(convert_video, instance.video_file.path, 1080)

    else:
        print("Video could not be converted due to slow upload speed")

"""
This is another version of the "video_post_save" function. In this function the videos are converted to 480p format only, without calculating 
the upload speed.

@receiver(post_save, sender = Video)
def video_post_save(sender, instance, created, **kwargs):

    queue = django_rq.get_queue('default', autocommit = True)
    queue.enqueue(convert_video, instance.video_file.path, 480)
"""

"""
Called whenever a video is deleted. It deletes the video file from the videos folder. Without this function video objects could be 
deleted from de database, however the deletion of these would not automatically delete their video files (which are stored in the 
videos folder, inside the media folder).
"""
@receiver(post_delete, sender = Video)
def video_post_delete(sender, instance, **kwargs): 
    
    if instance.video_file:

        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
