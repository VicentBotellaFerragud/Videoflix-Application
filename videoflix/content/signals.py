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
    
    speed_test = speedtest.Speedtest()
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
Called whenever a video is deleted. It deletes the video file from the videos folder. Without this function video objects could be 
deleted from de database, however the deletion of these would not automatically delete their video files (which are stored in the 
videos folder, inside the media folder).
"""
@receiver(post_delete, sender = Video)
def video_post_delete(sender, instance, **kwargs): 
    
    if instance.video_file:

        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            video_path_as_str = str(instance.video_file.path)
            same_video_with_480p_format_path = video_path_as_str[:-4] + '_480p.mp4'

            if same_video_with_480p_format_path:
                os.remove(same_video_with_480p_format_path)
