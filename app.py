import webview # ...

def main():
    window = webview.create_window('Spotify', 'https://play.geforcenow.com/mall/', width=800, height=600)
    webview.start()

if __name__ == '__main__':
    main()
