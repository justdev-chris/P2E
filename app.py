import webview
import keyboard

# URL for Ultimate Cat Clicker
URL = "https://catsdevs.online/Ultimate-Cat-Clicker/UCC/"

# Create window (comfy size, not fullscreen)
window = webview.create_window(
    "Ultimate Cat Clicker",
    URL,
    width=1000,
    height=700,
    resizable=True
)

# Toggle fullscreen with F11
def toggle_fullscreen():
    if window.fullscreen:
        window.fullscreen = False
        webview.resize_window(window, 1000, 700)
    else:
        window.fullscreen = True

# Hotkey binding
keyboard.add_hotkey("F11", toggle_fullscreen)

# Start app
webview.start()