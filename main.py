from src.gui import start_gui
from src.hotkey import setup_hotkey

if __name__ == "__main__":
    setup_hotkey()  # Set up the hotkey to toggle the GUI
    start_gui()     # Start the GUI