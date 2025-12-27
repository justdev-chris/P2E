import webview # ...

def main():
    window = webview.create_window('Geforce Now', 'https://play.geforcenow.com/mall/', fullscreen=True)
    webview.start()

if __name__ == '__main__':
    main()
