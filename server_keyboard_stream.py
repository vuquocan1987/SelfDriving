# # 

# #   # The server's hostname or IP address
# #         # The port used by the server

# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #     s.connect((HOST, PORT))
# #     s.sendall(b'Hello, world')
# #     data = s.recv(1024)

# # print('Received', repr(data))

import socket
import time
from pynput import keyboard
from queue import Queue


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

######################################################3
message = ''
keys = []

accept_keys = ['a','d','Key.up','Key.down','Key.right','Key.left']
stop_key = "Key.space"
exit_key = "Key.esc"


queue = Queue()

def write_keys(keys):
    global message
    for key in keys:
        message = str(key).replace(f'{chr(39)}', '')
        queue.put(message)
def on_press(key):
    global keys
    keys.append(key)
    write_keys(keys)
    keys = []

keyboard_thread = keyboard.Listener(on_press=on_press)
keyboard_thread.start()

print("[INFO] Create new socket server")
client_socket,addr= get_client_socket()
print("[INFO] Accept connection from ", addr[0], addr[1] )
time_out = 0.2
key_dct = {}
while True:
    # time_start = time.time()
    print("IT IS IN WHILE")
    try:
        messages = queue.get(timeout=time_out)
    except Exception as e:
        print("TIME OUT ROI MAN")
        messages = 'RELEASE'


    # print(messages)
    if client_socket:
        print(messages, '\n')
        if messages == exit_key:
            client_socket.sendall('EXIT'.encode())
            with open('data/keys.csv', 'w') as f:
                for key in key_dct.keys():
                    f.write("%s,%s\n"%(key,key_dct[key]))
            break
        #STOP SIGNAL
        elif messages == stop_key:
            client_socket.sendall('STOP'.encode())
            key_dct[str(int(time.time()*1000))] = messages

        elif messages not in accept_keys:
            client_socket.sendall('RELEASE'.encode())
            key_dct[str(int(time.time()*1000))] = messages

        else:
            client_socket.sendall(messages.encode())
            key_dct[str(int(time.time()*1000))] = messages

        print("connect")

client_socket.close()