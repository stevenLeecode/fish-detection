import socket

def server():
    SERVER_IP = '0.0.0.0'
    PORT = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_IP, PORT))
    s.listen(1)
    print(f"Server listening on {SERVER_IP}:{PORT}")

    conn, addr = s.accept()
    print(f"Connection from {addr} established.")

    file_name = conn.recv(1024).decode()
    print(f"Receiving file: {file_name}")
    file_size = int(conn.recv(1024).decode())
    print(f"File size: {file_size} bytes")

    file = open(file_name, 'wb')
    file_bytes = b""

    done = False
    while not done:
        data = conn.recv(1024)
        if file_bytes[-5:] == b"<END>":
            done = True
        else:
            file_bytes += data

    file.write(file_bytes[:-5])
    file.close()
    s.close()
    conn.close()

if __name__ == "__main__":
    server()