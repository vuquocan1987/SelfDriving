import numpy as np
import os
import cv2
import sys
print(cv2.version)
os.environ['DISPLAY'] = ':0'

URL = 'http://10.42.0.163:8080/video'

vid = cv2.VideoCapture(URL)
# vid.set()
vid.set(cv2.CAP_PROP_FPS,30)

ret, frame = vid.read()