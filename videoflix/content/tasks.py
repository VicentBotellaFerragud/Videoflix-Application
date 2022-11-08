import subprocess

def convert480p(source):

    target = source[:-4] + '_480p.mp4'   
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)    
    subprocess.run(cmd, shell = True)

"""
For the moment videos are only converted to 480p format.

def convert720p(source):

    target = source[:-4] + '_720p.mp4'   
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)    
    subprocess.run(cmd, shell = True)
 """
 