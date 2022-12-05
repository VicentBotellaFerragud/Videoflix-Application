import os
from django.dispatch import receiver
from .models import Video
from django.db.models.signals import post_save, post_delete
from .tasks import convert_video
import django_rq
import speedtest

def calculate_upload_speed():
    
    speed_test = speedtest.Speedtest(secure = True)
    # speed_test.get_best_server() see if this returns something
    upload_speed = speed_test.upload() 
    upload_speed_in_mbs = round(upload_speed / (10**6), 2)

    return upload_speed_in_mbs

@receiver(post_save, sender = Video)
def video_post_save(sender, instance, created, **kwargs): 

    if created:
        upload_speed_in_mbs = calculate_upload_speed()

        # see how ifs are evaluated by python

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
This is another version of the "video_post_save" function. In this function the videos are converted to 480p format only, without 
calculating the upload speed.

@receiver(post_save, sender = Video)
def video_post_save(sender, instance, created, **kwargs):

    queue = django_rq.get_queue('default', autocommit = True)
    queue.enqueue(convert_video, instance.video_file.path, 480)
"""

@receiver(post_delete, sender = Video)
def video_post_delete(sender, instance, **kwargs): 
    
    if instance.video_file: # think of changing file names before storing videos in the database file_exists = exists(path_to_file) from os.path import exists

        if os.path.isfile(instance.video_file.path): # ../../Sunset.mp4  ../../Sunset_480p.mp4 
            os.remove(instance.video_file.path) # try python "file exists"
            delete_converted_videos(instance.video_file.path, 480)
            delete_converted_videos(instance.video_file.path, 720)
            delete_converted_videos(instance.video_file.path, 1080)

def delete_converted_videos(video_path, video_format):

    try: 
        converted_video = video_path[:-4] + '_{}p.mp4'.format(video_format)
        os.remove(converted_video)

    except Exception:
        pass
