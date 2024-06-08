import socket

import scripts.log as log

HEADER = 64
FORMAT = 'utf-8'

ADDRESS = "127.0.0.1"
PORT = 4444

def main():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ADDRESS, PORT))
        log.ok("Connected to server")

        while True:
            msg = input('> ')
            if msg == 'QUIT':
                send(client, '!CYA')
                break
            elif msg == 'FILE':
                file_path = input("What file would you like: ")
                send(client, f"!FILE;{file_path}")
                download_file(client)
            else:
                send(client, msg)
    except KeyboardInterrupt:
        log.ok("Closed connection")
        send(client, '!CYA')

def send(conn, msg):
    message = msg.encode(FORMAT)
    send_length = str(len(message)).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def recive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    data = conn.recv(int(msg_length)).decode(FORMAT)
    return data

def download_file(conn):
    name = recive(conn)
    print(name)
    if name == "!ERR":
        log.fail("The file you requested doesn't exist on the server!")
    else:
        file_content = []
        downloading = True
        total_packages = recive(conn)
        while downloading:
            length = conn.recv(HEADER).decode(FORMAT)
            msg_content = conn.recv(int(length))
            file_content.append(msg_content)
            progress = len(file_content) - 1
            print(f"{progress}/{total_packages}")
            if progress == total_packages:
                downloading = False
                print("finsihed")
        print(file_content)
if __name__ == '__main__':
    main()
