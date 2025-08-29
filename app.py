import webview
import threading
import keyboard  # make sure 'keyboard' module is installed

window = webview.create_window(
    "Ultimate Cat Clicker",
    "https://catsdevs.online/Ultimate-Cat-Clicker/UCC/",
    width=900,
    height=600,
    resizable=True
)

def fullscreen_control():
    while True:
        key = keyboard.read_event()
        if key.event_type == keyboard.KEY_DOWN:
            if key.name == "f11":
                window.toggle_fullscreen()
            elif key.name == "esc" and window.fullscreen:
                window.toggle_fullscreen()  # ESC exits fullscreen

threading.Thread(target=fullscreen_control, daemon=True).start()
webview.start(debug=True)