from pynput import keyboard
import cv2
import time

st = time.time()
THRESHOLD = .1
def save_input(key):
    global st
    if time.time() - st < THRESHOLD:
        return
    st = time.time()
    print(f"you just press: {key}")
    print(type(key))

def reset_time(key):
    print('on release')
    st = time.time() - THRESHOLD - 1

keyboard_thread = keyboard.Listener(on_press=save_input, on_release=reset_time)

keyboard_thread.start()

time.sleep(10000)