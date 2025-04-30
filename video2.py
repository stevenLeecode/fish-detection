from picamera2 import Picamera2, Preview
from datetime import datetime
import time
import subprocess
from picamera2.encoders import H264Encoder
import os
import numpy as np
import cv2
import socket
import struct
import pickle

client_socket = socket.socket()
desktop_addr = ('192.168.2.241', 12345)
client_socket.connect(desktop_addr)

def send_server(data, length): 
    client_socket.sendall(struct.pack(">L", length) + data)
    print("Sent to server.")

#Setup
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size":(640, 640)})
picam2.configure(config)

time.sleep(2)

picam2.start()

time.sleep(4)

img_counter = 0 
while True:
    frame = picam2.capture_array()
    _, img_encoded = cv2.imencode('.jpg', frame)
    data = pickle.dumps(img_encoded, 0)
    size = len(data)
    print("length: ", size)
    print("image_counter: ", img_counter)
    img_counter += 1
    send_server(data, size)