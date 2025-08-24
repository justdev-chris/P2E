import webview
import time

# Splash screen window (frameless, for smooth effect)
splash = webview.create_window(
    'Loading...', 
    'https://i.imgur.com/gDFZh7W.jpeg', 
    width=600, 
    height=400, 
    resizable=False, 
    frameless=True
)

def show_splash_then_main():
    # Show splash for 10 seconds
    time.sleep(10)
    
    # Fade out effect (simulate by gradually reducing alpha)
    for alpha in range(100, -1, -5):
        splash.evaluate_js(f"document.body.style.opacity = '{alpha/100}'")
        time.sleep(0.05)
    
    # Close splash
    splash.destroy()
    
    # Open main fullscreen website window
    main_window = webview.create_window('TF2', 'https://play.geforcenow.com/games?game-id=40512534-ad27-4a12-afa7-6fc412288072&lang=en_US&asset-id=01_547b2064-13ad-4ba5-b928-d2770accddf1', fullscreen=True)
    webview.start()

webview.start(show_splash_then_main, window=splash)
