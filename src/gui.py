import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from src.network import send_file

def on_drop(event, peer_ip):
    file_path = event.data.strip('{}')
    print(f"File dropped: {file_path}")
    send_file(peer_ip, 5005, file_path)  # Send file to the selected peer

def start_gui():
    root = TkinterDnD.Tk()
    root.title("File Sharing App")

    label = tk.Label(root, text="Drag and drop files here", width=50, height=10)
    label.pack()

    # Example peer (you can dynamically load peers from peers.json)
    peer_ip = "192.168.1.10"
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', lambda event: on_drop(event, peer_ip))

    root.mainloop()