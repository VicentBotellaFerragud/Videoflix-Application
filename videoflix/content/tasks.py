import subprocess

# command for converting videos --> ffmpeg -i "PATH" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "TARGET PATH"

def convert480p(source):

    target = source + '_480p.mp4'   
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)    
    subprocess.run(cmd, shell = True, cwd = 'C:\\Users\\vicen\\Desktop\\Programació\\Weiterbildung-Developer-Akademie\\Back-end_projects\\Videoflix-Application\\videoflix\\media\\videos')

def convert720p(source):

    target = source + '_720p.mp4'   
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)    
    run = subprocess.run(cmd, capture_output = True)
 