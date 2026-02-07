from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QMouseEvent, QPixmap, QPainter, QColor, QPen


class Capture(QWidget):
    def __init__(self, main_window, pixmap):
        super().__init__()
        self.main = main_window
        self.pixmap = pixmap  # kogu ekraani pilt

        self.setMouseTracking(True)
        # leiame ekraanide ühendatud ala (multi-monitor)
        screens = QApplication.screens()
        virtual_rect = QRect()
        for screen in screens:
            virtual_rect = virtual_rect.united(screen.geometry())
        self.setGeometry(virtual_rect)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setCursor(Qt.CrossCursor)
        QApplication.setOverrideCursor(Qt.CrossCursor)

        self.origin = QPoint()  # alguspunkt
        self.current = QPoint()  # praegune asukoht
        self.selecting = False

        self.show()

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.current = event.pos()
            self.selecting = True
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if self.selecting:
            self.current = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.selecting = False
            self.update()

            rect = QRect(self.origin, self.current).normalized()
            if not rect.isEmpty():
                # lõikame valitud ala originaalpildist
                captured = self.pixmap.copy(rect)

                # paneme pildi lõikelauale
                clipboard = QApplication.clipboard()
                clipboard.setPixmap(captured)

                # kuvame pisipildi peamises aknas
                display_pixmap = captured.scaled(400, 420, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.main.label.setPixmap(display_pixmap)
                self.main.original_pixmap = captured

                # koordinaadid (top-left & bottom-right+1)
                tl_x = rect.left()
                tl_y = rect.top()
                br_x = rect.right() + 1
                br_y = rect.bottom() + 1
                coords_text = f"({tl_x}, {tl_y}, {br_x}, {br_y})"

                self.main.coords_label.setText(coords_text)
                self.main.coords_label.setVisible(True)
                self.main.copy_btn.setVisible(True)
                self.main.btn_save.setVisible(True)
                self.main.copy_image_btn.setVisible(True)

                # paneme koordinaadid lõikelauale
                clipboard.setText(coords_text)

                self.main.show()

            QApplication.restoreOverrideCursor()
            self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        # joonistame kogu ekraanipildi taustaks
        painter.drawPixmap(0, 0, self.width(), self.height(), self.pixmap)

        dim_color = QColor(0, 0, 0, 160)  # tumedam vari

        if not self.selecting:
            # kui valikut pole veel tehtud, tume ala ekraanide ulatuses
            painter.fillRect(self.rect(), dim_color)
        else:
            rect = QRect(self.origin, self.current).normalized()

            # tumedam ala väljaspool valikut
            painter.fillRect(0, 0, self.width(), rect.top(), dim_color)
            painter.fillRect(0, rect.bottom() + 1, self.width(), self.height() - rect.bottom() - 1, dim_color)
            painter.fillRect(0, rect.top(), rect.left(), rect.height(), dim_color)
            painter.fillRect(rect.right() + 1, rect.top(), self.width() - rect.right() - 1, rect.height(), dim_color)

            # sinine joon ümber valitud ala
            painter.setPen(QPen(Qt.blue, 2, Qt.DashLine))
            painter.drawRect(rect)
