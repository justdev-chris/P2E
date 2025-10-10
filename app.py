import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

class CustomDesktop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("catgui")
        self.showMaximized()  # Full screen

        # Video wallpaper
        self.video_widget = QVideoWidget(self)
        self.video_widget.setGeometry(0, 0, self.width(), self.height())
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatioByExpanding)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(10)  # Mute wallpaper audio
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile(r"C:\Users\moren\Downloads\boykisser-meme.gif"))  # Replace with your video
        self.media_player.setLoops(-1)  # Loop indefinitely
        self.media_player.play()

        # Taskbar
        self.taskbar = QWidget(self)
        self.taskbar.setStyleSheet("background-color: rgba(0,0,0,180);")
        self.taskbar.setFixedHeight(50)
        self.taskbar_layout = QHBoxLayout()
        self.taskbar.setLayout(self.taskbar_layout)

        # Example apps (replace with paths to real executables)
        apps = {
            "Notepad": r"C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11.2507.26.0_x64__8wekyb3d8bbwe\Notepad\Notepad.exe",
            "Paint": r"C:\Program Files\WindowsApps\Microsoft.Paint_11.2508.361.0_x64__8wekyb3d8bbwe\PaintApp\mspaint.exe",
            "Discord": r"C:\Users\moren\OneDrive\Desktop\Discord.lnk",
            "Microsoft Edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "Minecraft": r"C:\Users\moren\OneDrive\Desktop\Minecraft.exe"
        }
        for name, path in apps.items():
            btn = QPushButton(name)
            btn.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
            btn.clicked.connect(lambda checked, p=path: self.launch_app(p))
            self.taskbar_layout.addWidget(btn)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.addWidget(self.taskbar)
        main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(main_layout)

    def launch_app(self, path):
        try:
            subprocess.Popen(path)
        except Exception as e:
            print(f"Failed to open {path}: {e}")

app = QApplication(sys.argv)
window = CustomDesktop()
window.show()
sys.exit(app.exec())
