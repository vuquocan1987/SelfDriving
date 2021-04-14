from pynput import keyboard
from pynput.keyboard import Key
import cv2
import time
import numpy as np
import os
import csv 

URL = 'http://192.168.224.21:8080/video'
IMAGE_PATH = 'data/images'
CSV_PATH = 'data/train.csv'
key_dict = {Key.up: 0, Key.down: 3, Key.left:2, Key.right:1}
vid = cv2.VideoCapture(URL)
vid.set(cv2.CAP_PROP_FPS,30)
vid.set(cv2.CAP_PROP_BUFFERSIZE,1)

st = time.time()
THRESHOLD = .1
frame = None

def save_input(key):
    global st
    if time.time() - st < THRESHOLD or key not in key_dict:
        return
    st = time.time()
    print(f"you just press: {key}")
    generate_data(key)

def generate_data(key):
    global frame
    key_code = key_dict[key]
    file_name = f'{time.time()}.{key_code}.jpg'
    # cv2.imshow('tmp',frame)
    # print(frame.shape)
    # cv2.waitKey(0)
    cv2.imwrite(f'{IMAGE_PATH}/{file_name}', frame)
    with open(CSV_PATH, mode='a') as employee_file:
        w = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([file_name, key_dict[key]])

def reset_time(key):
    
    print('on release')
    st = time.time() - THRESHOLD - 1

keyboard_thread = keyboard.Listener(on_press=save_input, on_release=reset_time)

keyboard_thread.start()

while True:
    ret, frame = vid.read()
    
time.sleep(10000)




