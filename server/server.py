import socket
import threading
import os

import log

PORT = 4444
ADDRESS = "0.0.0.0"

SERVER_DIR = '/home/aexyzk/server/'

HEADER = 64
SPLIT_SIZE = 4096
FORMAT = 'utf-8'

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDRESS, PORT))
except OSError:
    log.fail("Port is in use")
    exit()

def send(conn, msg):
    message = msg.encode(FORMAT)
    send_length = str(len(message)).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def handle_client(conn, addr):
    log.ok(f"Client from {addr} connected")
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length != '':
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == '!CYA':
                break
            elif msg[:5] == '!FILE':
                file_path = os.path.join(SERVER_DIR, msg.split(';')[1])
                log.info(f"Client requested: {file_path}")
                
                if os.path.isfile(file_path):
                    send(conn, msg.split(';')[1])
                    with open(file_path, 'rb') as file:
                        file_content = file.read()
                        out = [(file_content[i:i+SPLIT_SIZE]) for i in range(0, len(file_content), SPLIT_SIZE)]
                        total_packages = int(len(file_content) / SPLIT_SIZE)
                        send(conn, str(total_packages))
                        for i, string in enumerate(out):
                            send_length = str(4096).encode(FORMAT)
                            send_length += b' ' * (HEADER - len(send_length))
                            conn.send(send_length)
                            conn.send(string)
                            log.info(f"Package {i}/{total_packages} sent to client!")
                    log.info(f"'{file_path}' sent to client {addr}")
                else:
                    log.info(f"{addr} tried to request '{file_path}' which does not exist: sending client error message")
                    send(conn, '!ERR')
            else:
                log.info(f"{addr}: {msg}")

def main():
    connected = False
    try:
        log.info("Server is starting!")
        server.listen()
        log.ok(f"Listoning on port {PORT}")
        while True:
            if connected != True:
                conn, addr = server.accept()
                connected = True 
                handle_client(conn, addr)
                connected = False
                log.ok("Client disconnected")
    except KeyboardInterrupt:
        log.ok("Killed process!")

if __name__ == '__main__':
    main()
