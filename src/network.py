import socket
import os
import threading

# Function to send a file with metadata
def send_file(ip, port, filepath, sender_name, recipient_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    # Send metadata: sender_name, recipient_name, file_name
    file_name = os.path.basename(filepath)
    metadata = f"{sender_name}|{recipient_name}|{file_name}".encode()
    sock.sendall(metadata + b"\n")  # Metadata ends with a newline

    # Send the file content
    with open(filepath, 'rb') as f:
        sock.sendfile(f)

    sock.close()

# Function to receive files with metadata
def receive_file(port, save_directory):
    def handle_client(conn, addr):
        try:
            # Read metadata (first line)
            metadata = conn.recv(1024).decode().strip()
            sender_name, recipient_name, file_name = metadata.split('|')

            print(f"Received file from {sender_name} intended for {recipient_name}: {file_name}")

            # Check if the file is intended for this peer
            if recipient_name != get_current_peer_name():
                print("File not intended for this peer. Ignoring.")
                conn.close()
                return

            # Save the file
            save_path = os.path.join(save_directory, file_name)
            with open(save_path, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)

            print(f"File saved: {save_path}")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            conn.close()

    # Start listening for incoming connections
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen(5)
    print(f"Listening for incoming files on port {port}...")

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

# Helper function to get the current peer's name
def get_current_peer_name():
    from src.config import load_peers
    peers = load_peers()
    for name, info in peers.items():
        if info["ip"] == get_local_ip():
            return name
    return "Unknown"

# Helper function to get the local IP address
def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip