import webview

# lil function to toggle fullscreen
def toggle_fullscreen(window):
    window.toggle_fullscreen()

def main():
    # create window (smaller, windowed)
    window = webview.create_window(
        "Ultimate Cat Clicker",
        "https://catsdevs.online/Ultimate-Cat-Clicker/UCC/",
        width=1000,
        height=700,
        resizable=True
    )

    # inject JS for F11 + Esc hotkeys
    def inject_hotkeys():
        window.evaluate_js("""
            document.addEventListener("keydown", function(e) {
                if (e.key === "F11") {
                    pywebview.api.toggle()
                    e.preventDefault()
                }
                if (e.key === "Escape") {
                    pywebview.api.toggle()
                    e.preventDefault()
                }
            });
        """)

    # start webview + expose toggle
    webview.start(
        func=inject_hotkeys,
        gui="edgechromium",
        debug=True,
        http_server=True,
        js_api={"toggle": lambda: toggle_fullscreen(window)},
        window=window
    )

if __name__ == "__main__":
    main()