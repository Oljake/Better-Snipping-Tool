import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from screen_region_selector import ScreenRegionSelector

# parem kvaliteet 4k / retina ekraanidel
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # tume teema
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
    selector.show()

    sys.exit(app.exec_())
