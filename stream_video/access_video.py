import cv2
import numpy as np
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://10.42.0.163:8080/video'

cap = cv2.VideoCapture(url)
# while(True):
#     ret, frame = cap.read()
#     if frame is not None:
#         cv2.imshow('frame',frame)
#     else:
#         print('None')
#     q = cv2.waitKey(1)
#     if q == ord("q"):
#         break
def get_frame():
    ret, frame = cap.read()
    if frame is None:
        raise Exception("Can't take take screenshot of camera")
    
cv2.destroyAllWindows()
