import webview # im js building lol

def main():
    window = webview.create_window('tf2', 'https://play.geforcenow.com/games?game-id=40512534-ad27-4a12-afa7-6fc412288072&lang=en_US&asset-id=01_547b2064-13ad-4ba5-b928-d2770accddf1', width=800, height=600)
    webview.start()

if __name__ == '__main__':
    main()
