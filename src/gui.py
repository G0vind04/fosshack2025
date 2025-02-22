import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from src.network import send_file, receive_file
from src.config import load_peers
import threading
import os

def on_drop(event, peer_ip, sender_name, recipient_name):
    file_path = event.data.strip('{}')
    print(f"File dropped: {file_path}")
    threading.Thread(target=send_file, args=(peer_ip, 5005, file_path, sender_name, recipient_name)).start()

def start_gui():
    peers = load_peers()  # Load peer configurations

    root = TkinterDnD.Tk()
    root.title("File Sharing App")
    root.geometry("400x200")

    # Create drop zones for each peer
    for peer_name, peer_info in peers.items():
        peer_ip = peer_info["ip"]
        position = peer_info["position"]

        frame = tk.Frame(root, width=180, height=150, bg="lightblue" if position == "left" else "lightgreen")
        frame.pack(side=tk.LEFT if position == "left" else tk.RIGHT, padx=10, pady=10)

        label = tk.Label(frame, text=f"Drop here for {peer_name}", bg="white")
        label.pack(expand=True, fill=tk.BOTH)

        # Enable drag-and-drop
        frame.drop_target_register(DND_FILES)
        frame.dnd_bind('<<Drop>>', lambda event, ip=peer_ip, sn=get_current_peer_name(), rn=peer_name: on_drop(event, ip, sn, rn))

    # Start file receiver in a background thread
    threading.Thread(target=receive_file, args=(5005, os.path.expanduser("~/Desktop"))).start()

    root.mainloop()

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