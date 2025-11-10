import tkinter as tk
from tkinter import messagebox
import requests
import sys

try:
    import tkinterweb
except ImportError:
    messagebox.showerror("Missing Library", "Please install tkinterweb: pip install tkinterweb")
    sys.exit()

def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def minimize_window(event=None):
    root.attributes("-fullscreen", False)
    root.state('iconic')  # Minimize to taskbar

if check_internet():
    root = tk.Tk()
    root.title("Ultimate Cat Clicker")
    
    # Start in fullscreen
    root.attributes("-fullscreen", True)
    
    # Bind ESC key to minimize
    root.bind("<Escape>", minimize_window)
    
    # Load website
    frame = tkinterweb.HtmlFrame(root)
    frame.load_url("https://catsdevs.online")
    frame.pack(fill="both", expand=True)
    
    root.mainloop()
else:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Offline", "Ultimate Cat Clicker requires an internet connection.")
    root.destroy()