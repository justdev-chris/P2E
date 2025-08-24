import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QPixmap, QImage

class Browser(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("TF2")
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)
        self.showFullScreen()

def load_pixmap_from_url(url):
    response = requests.get(url)
    image = QImage.fromData(response.content)
    return QPixmap.fromImage(image)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Use a hosted image URL
    image_url = "https://i.imgur.com/gDFZh7W.jpeg"
    pixmap = load_pixmap_from_url(image_url)
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.show()

    # Fade out after 10 seconds
    def fade_splash():
        animation = QPropertyAnimation(splash, b"windowOpacity")
        animation.setDuration(1000)  # 1 second fade
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.start()
        animation.finished.connect(lambda: splash.close())

    QTimer.singleShot(10000, fade_splash)  # show splash 10s
    QTimer.singleShot(11000, lambda: Browser("https://play.geforcenow.com/games?game-id=40512534-ad27-4a12-afa7-6fc412288072&lang=en_US&asset-id=01_547b2064-13ad-4ba5-b928-d2770accddf1").show())  # show browser after fade

    sys.exit(app.exec_())
