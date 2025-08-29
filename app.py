import webview

def main():
    # custom title for the window
    window = webview.create_window(
        title="Ultimate Cat Clicker",
        url="https://catsdevs.online/Ultimate-Cat-Clicker/uccv3-CHAPTER2/",  # you can change this to any site or local file
        fullscreen=True
    )

    # start the webview loop
    webview.start()

if __name__ == "__main__":
    main()