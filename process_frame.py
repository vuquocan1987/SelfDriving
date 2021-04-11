import cv2
import numpy as np
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://10.42.0.163:8080/video'
cap = cv2.VideoCapture(url)

def get_frame():
    ret, frame = cap.read()
    if frame is None:
        raise Exception("Can't take take screenshot of camera")
    frame = np.mean(frame, axis=-1)
    print(frame.shape)