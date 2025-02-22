import keyboard
from tkinter import Tk

root = None  # Global reference to the Tkinter root window

def toggle_gui():
    if root.state() == "normal":
        root.withdraw()  # Hide the window
    else:
        root.deiconify()  # Show the window

def setup_hotkey():
    keyboard.add_hotkey('ctrl+shift+f', toggle_gui)