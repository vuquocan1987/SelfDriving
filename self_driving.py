from matplotlib.pyplot import axis
from pynput import keyboard
from pynput.keyboard import Key
import cv2
import time
import numpy as np
import os
import csv
from constant import PATHS
import socket
# URL = 'http://10.42.0.163:8080/video'
URL = 'http://192.168.224.21:8080/video'

key_dict = {Key.up: 0, Key.down: 3, Key.left:2, Key.right:1}
code_to_message = {v: str(k) for k,v in key_dict.items()}
print(code_to_message)
rev_key_dict = {v:k for k,v in key_dict.items()}
model = cv2.ml.ANN_MLP_load(PATHS.MODEL)
vid = cv2.VideoCapture(URL)
vid.set(cv2.CAP_PROP_FPS,30)
vid.set(cv2.CAP_PROP_BUFFERSIZE,1)
dims = 320*240


def get_client_socket():
    HOST = '0.0.0.0'
    PORT = 1111
# Create a stream based socket(i.e, a TCP socket)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind and listen
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(5)
    return serverSocket.accept()
def get_key(img):
    img = preprocess_img(img)
    ret, resp = model.predict(img)
    prediction = resp.argmax(-1)
    key = code_to_message[prediction[0]]
    return key
def preprocess_img(img):
    img = np.mean(img, axis = -1)
    img = np.reshape(img, dims)
    img = np.expand_dims(img, axis = 0)
    return img
client_socket, addr = get_client_socket()
while True:
    ret, frame = vid.read()
    if frame is not None:
        key = get_key(frame)
        client_socket.sendall(key.encode())
    else:
        print("frame is none")
    



