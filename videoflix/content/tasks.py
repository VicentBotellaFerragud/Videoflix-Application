import subprocess


def convert_video(source, video_format):
    target = source[:-4] + '_{}p.mp4'.format(video_format)   
    cmd = 'ffmpeg -i "{}" -s hd{} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, video_format, target)    
    subprocess.run(cmd, shell = True)
