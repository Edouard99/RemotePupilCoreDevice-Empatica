import time
# i=0
# while(i<3):
#     time.sleep(1)
#     i+=1
#     print(i)
from video_backend import VideoBackEnd
crash=True
while(crash):
    try :
        print("hello")
        ip = "127.0.0.1"  # ip address of remote pupil or localhost
        port = "50020"  # same as in the pupil remote gui
        pupilbackend = VideoBackEnd(ip, port)
        pupilbackend.start("eye0")  # default is "world". Other options are "eye0" and "eye1".
        crash=False
    except Exception as e:
        crash=True