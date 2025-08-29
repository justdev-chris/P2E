import webview

def main():
    # custom title for the window
    window = webview.create_window(
        title="Ultimate Cat Clicker",
        url="https://catsdevs.online/Ultimate-Cat-Clicker/UCC/", 
        fullscreen=True
    )

    webview.start()

if __name__ == "__main__":
    main()
