import socket,cv2, pickle,struct
import numpy as np
import base64
import time

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host_ip = 'localhost'
# host_ip = '192.168.43.53'
# host_ip = "192.168.224.29"
host_ip = "10.42.0.98"
# port = 9999
# port = 6666
port = 1111
client_socket.connect((host_ip,port)) # a tuple
data = b''
# payload_size = struct.calcsize("Q")
payload_size = struct.calcsize("<L")

# print('payload size: ', payload_size)
count = 0
img_dct = {}
import os
os.makedirs('data', exist_ok = True)
os.makedirs('data/images', exist_ok = True)
while True:
    count +=1
    print(count)
    while len(data) < payload_size:
        # data += client_socket.recv(4096)
        data += client_socket.recv(128*1024)
        
    # Get the frame size and remove it from the data.
    frame_size = struct.unpack("<L", data[:payload_size])[0]
    data = data[payload_size:]
    while len(data) < frame_size:
        data += client_socket.recv(128*1024)
    # Cut the frame to the beginning of the next frame.
    frame_data = data[:frame_size]
    data = data[frame_size:]
    # Converting the image to be sent.
    img = base64.b64decode(frame_data)
    npimg = np.fromstring(img, dtype=np.uint8)
    frame = cv2.imdecode(npimg, 1)

    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    if count % 5 == 0:
        cv2.imwrite(f'data/images/rc-{count:06d}'+'.jpg',frame)
        img_dct[str(int(time.time()*1000))] = f'rc-{count:06d}'+'.jpg'
    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == 27 :
        with open('data/images.csv', 'w') as f:
            for key in img_dct.keys():
                f.write("%s,%s\n"%(key,img_dct[key]))
        break

client_socket.close()