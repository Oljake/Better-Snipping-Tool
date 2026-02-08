import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from screen_region_selector import ScreenRegionSelector

# High DPI support
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller --onefile"""
    try:
        # PyInstaller temp folder
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(resource_path("icon.ico")))

    # Dark theme
    app.setStyleSheet("""
    QFrame { background-color: #3f3f3f; }
    QLabel { color: white; font-weight: bold; font-size: 14px; }
    QPushButton {
        border-radius: 5px;
        background-color: rgb(60, 90, 255);
        padding: 10px;
        color: white;
        font-weight: bold;
        font-family: Arial;
        font-size: 12px;
    }
    QPushButton:hover { background-color: rgb(60, 20, 255); }
    """)

    selector = ScreenRegionSelector()
    selector.setWindowTitle("Better Snipping Tool")     # ← window title
    selector.show()

    sys.exit(app.exec_())
