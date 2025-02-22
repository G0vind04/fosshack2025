import socket
import os

def discover_peers():
    peers = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(b"DISCOVER", ('<broadcast>', 5005))
    sock.settimeout(2)
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            if data == b"ACK":
                peers.append(addr[0])
    except socket.timeout:
        pass
    sock.close()
    return peers

def send_file(ip, port, filepath):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    with open(filepath, 'rb') as f:
        sock.sendfile(f)
    sock.close()

def receive_file(port, save_path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen(1)
    conn, addr = sock.accept()
    with open(save_path, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
    conn.close()
    sock.close()