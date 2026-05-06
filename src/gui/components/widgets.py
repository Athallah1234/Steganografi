from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent

class ImageDropArea(QLabel):
    fileDropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("previewArea")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Tarik & Lepas Gambar ke Sini\natau Klik untuk Memilih")
        self.setAcceptDrops(True)
        self.setMinimumSize(300, 200)
        self.setScaledContents(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.fileDropped.emit(files[0])

    def set_image(self, path: str):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            # Maintain aspect ratio for preview
            self.setPixmap(pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.setText("")
        else:
            self.setText("Gagal memuat gambar")
