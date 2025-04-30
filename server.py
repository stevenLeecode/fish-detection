import socket
import cv2
import numpy as np
import struct
import pickle
from fish_model import load_models, process_frame

def server():

    SERVER_IP = '0.0.0.0'
    PORT = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_IP, PORT))
    s.listen(1)
    print(f"Server listening on {SERVER_IP}:{PORT}")

    conn, addr = s.accept()
    print(f"Connection from {addr} established.")

    #Initialize models
    model, tracker, track_history = load_models()

    data = b''
    payload_size = struct.calcsize(">L")
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        frame = process_frame(frame, model, tracker)
        cv2.imshow("YOLO11 Tracking", frame)

        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    conn.close()
    s.close()

if __name__ == "__main__":
    server()