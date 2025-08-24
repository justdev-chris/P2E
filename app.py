import webview
import threading
import time
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# --- Splash screen function with progress bar ---
def show_splash():
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)
    splash_root.geometry("600x400+300+150")
    splash_root.attributes('-alpha', 1.0)  # fully opaque

    # Load image from URL
    response = requests.get("https://i.imgur.com/gDFZh7W.jpeg")
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((600, 400))
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(splash_root, image=photo)
    label.pack()

    # Progress bar
    progress = tk.DoubleVar()
    progress_bar = tk.Canvas(splash_root, width=400, height=20, bg="white")
    progress_bar.place(x=100, y=360)
    bar = progress_bar.create_rectangle(0, 0, 0, 20, fill="green")

    splash_root.update()

    # Animate progress bar while showing splash for 6 seconds
    for i in range(200):
        progress_width = (i+1) * (400/60)  # 400px full width
        progress_bar.coords(bar, 0, 0, progress_width, 20)
        splash_root.update()
        time.sleep(0.1)

    # Fade out over 1 second
    for i in range(20):
        alpha = 1.0 - (i / 20)
        splash_root.attributes('-alpha', alpha)
        splash_root.update()
        time.sleep(0.05)

    splash_root.destroy()

# --- Main webview function ---
def open_main_app():
    time.sleep(0.1)
    window = webview.create_window(
        "TF2", 
        "https://play.geforcenow.com/games?game-id=40512534-ad27-4a12-afa7-6fc412288072&lang=en_US&asset-id=01_547b2064-13ad-4ba5-b928-d2770accddf1",
        fullscreen=True
    )
    webview.start(window)

# --- Run splash in a thread ---
splash_thread = threading.Thread(target=show_splash)
splash_thread.start()

# --- After splash, run main app ---
open_main_app()
