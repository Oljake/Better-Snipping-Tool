from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QFileDialog,
    QApplication,
)
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap

from capture import Capture


class ScreenRegionSelector(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.setWindowTitle("Screen Capturer")
        self.setFixedSize(400, 500)

        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)
        lay = QVBoxLayout(frame)
        lay.setAlignment(Qt.AlignCenter)
        lay.setContentsMargins(5, 5, 5, 5)

        self.label = QLabel()  # siia tuleb pisike eelvaade
        self.btn_capture = QPushButton("Capture")
        self.btn_capture.clicked.connect(self.capture)

        self.coords_label = QLabel()
        self.coords_label.setVisible(False)
        self.coords_label.setWordWrap(False)

        self.copy_btn = QPushButton("Copy Coords")
        self.copy_btn.clicked.connect(self.copy_coords)
        self.copy_btn.setVisible(False)

        # koordinaatide rida + nupp
        coords_lay = QHBoxLayout()
        coords_lay.addWidget(self.coords_label)
        coords_lay.addWidget(self.copy_btn)

        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save)
        self.btn_save.setVisible(False)

        self.copy_image_btn = QPushButton("Copy Image")
        self.copy_image_btn.clicked.connect(self.copy_image)
        self.copy_image_btn.setVisible(False)

        # salvestamise ja kopeerimise nupud
        actions_lay = QHBoxLayout()
        actions_lay.addWidget(self.copy_image_btn)
        actions_lay.addWidget(self.btn_save)

        # kõik kokku
        lay.addWidget(self.label)
        lay.addLayout(coords_lay)
        lay.addWidget(self.btn_capture)
        lay.addLayout(actions_lay)

        self.setCentralWidget(frame)
        self.original_pixmap = QPixmap()  # valitud ala originaal

    def capture(self):
        self.hide()  # peidame akna enne pildistamist
        QTimer.singleShot(300, self._delayed_capture)  # väike viivitus, et aken jõuaks kaduda

    def _delayed_capture(self):
        # leiame kõigi ekraanide ühendatud ala
        screens = QApplication.screens()
        virtual_rect = QRect()
        for screen in screens:
            virtual_rect = virtual_rect.united(screen.geometry())

        # teeme täisekraani pildi (kõik monitorid)
        pixmap = QApplication.primaryScreen().grabWindow(
            0, virtual_rect.x(), virtual_rect.y(),
            virtual_rect.width(), virtual_rect.height()
        )

        self.capturer = Capture(self, pixmap)

    def save(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "Image files (*.png *.jpg *.bmp)"
        )
        if file_name:
            self.original_pixmap.save(file_name)

    def copy_coords(self):
        QApplication.clipboard().setText(self.coords_label.text())

    def copy_image(self):
        QApplication.clipboard().setPixmap(self.original_pixmap)
