import os
import pyperclip
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QPushButton, QTextEdit, QLineEdit, QProgressBar, QLabel, 
    QFileDialog, QMessageBox, QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt, QThread, Signal
from src.core.image.lsb import LSBSteg
from src.crypto.encryption import EncryptionManager
from src.gui.components.widgets import ImageDropArea
from src.gui.styles import DARK_STYLE
from src.utils.logger import logger

class WorkerThread(QThread):
    finished = Signal(bool, str)
    progress = Signal(int)

    def __init__(self, task_type, **kwargs):
        super().__init__()
        self.task_type = task_type
        self.kwargs = kwargs

    def run(self):
        try:
            if self.task_type == "encode":
                password = self.kwargs.get('password')
                message = self.kwargs.get('message')
                img_path = self.kwargs.get('img_path')
                out_path = self.kwargs.get('out_path')
                
                # Encrypt first
                encrypted_data = EncryptionManager.encrypt(message, password)
                
                # Then steganography
                LSBSteg.encode(img_path, encrypted_data, out_path, self.progress.emit)
                self.finished.emit(True, out_path)
                
            elif self.task_type == "decode":
                img_path = self.kwargs.get('img_path')
                password = self.kwargs.get('password')
                
                # Extract stego data
                encrypted_data = LSBSteg.decode(img_path, self.progress.emit)
                
                # Decrypt
                message = EncryptionManager.decrypt(encrypted_data, password)
                self.finished.emit(True, message)
                
        except Exception as e:
            self.finished.emit(False, str(e))

class AegisVaultApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AegisVault - Secure Image Steganography")
        self.resize(1000, 700)
        self.current_theme = "dark"
        self.setStyleSheet(DARK_STYLE)
        
        self.current_img_path = None
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        header_layout = QHBoxLayout()
        header = QLabel("AEGIS VAULT")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #3b82f6;")
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        self.theme_btn = QPushButton("🌙 Dark Mode")
        self.theme_btn.setObjectName("secondaryBtn")
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(header_layout)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_encode_tab(), "🔐 Encode (Sembunyikan)")
        self.tabs.addTab(self.create_decode_tab(), "🔓 Decode (Ekstrak)")
        main_layout.addWidget(self.tabs)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Status Bar
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)

    def create_encode_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)

        # Left side: Image selection
        left_panel = QVBoxLayout()
        self.encode_drop_area = ImageDropArea()
        self.encode_drop_area.fileDropped.connect(self.handle_file_dropped)
        self.encode_drop_area.mousePressEvent = lambda e: self.browse_image()
        left_panel.addWidget(QLabel("1. Pilih Gambar Dasar (PNG)"))
        left_panel.addWidget(self.encode_drop_area)
        layout.addLayout(left_panel, 1)

        # Right side: Message and Password
        right_panel = QVBoxLayout()
        
        # Message Group
        msg_group = QGroupBox("2. Masukkan Pesan Rahasia")
        msg_layout = QVBoxLayout(msg_group)
        self.encode_msg_input = QTextEdit()
        self.encode_msg_input.setPlaceholderText("Tulis pesan yang ingin disembunyikan di sini...")
        msg_layout.addWidget(self.encode_msg_input)
        right_panel.addWidget(msg_group)

        # Security Group
        sec_group = QGroupBox("3. Keamanan & Output")
        sec_layout = QFormLayout(sec_group)
        self.encode_pass_input = QLineEdit()
        self.encode_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.encode_pass_input.setPlaceholderText("Password Enkripsi")
        
        pass_toggle = QPushButton("👁")
        pass_toggle.setFixedWidth(30)
        pass_toggle.setObjectName("secondaryBtn")
        pass_toggle.clicked.connect(lambda: self.toggle_pass_visibility(self.encode_pass_input))
        
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(self.encode_pass_input)
        pass_layout.addWidget(pass_toggle)
        
        sec_layout.addRow("Password:", pass_layout)
        
        self.encode_btn = QPushButton("Mulai Encode & Simpan")
        self.encode_btn.clicked.connect(self.start_encode)
        sec_layout.addRow(self.encode_btn)
        
        right_panel.addWidget(sec_group)
        layout.addLayout(right_panel, 1)

        return tab

    def create_decode_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)

        # Left side: Image selection
        left_panel = QVBoxLayout()
        self.decode_drop_area = ImageDropArea()
        self.decode_drop_area.fileDropped.connect(self.handle_file_dropped)
        self.decode_drop_area.mousePressEvent = lambda e: self.browse_image()
        left_panel.addWidget(QLabel("Pilih Gambar Steganografi (PNG)"))
        left_panel.addWidget(self.decode_drop_area)
        layout.addLayout(left_panel, 1)

        # Right side: Password and Result
        right_panel = QVBoxLayout()
        
        # Security Group
        sec_group = QGroupBox("Otorisasi")
        sec_layout = QFormLayout(sec_group)
        self.decode_pass_input = QLineEdit()
        self.decode_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        sec_layout.addRow("Password:", self.decode_pass_input)
        
        self.decode_btn = QPushButton("Ekstrak Pesan")
        self.decode_btn.clicked.connect(self.start_decode)
        sec_layout.addRow(self.decode_btn)
        right_panel.addWidget(sec_group)

        # Result Group
        res_group = QGroupBox("Hasil Decode")
        res_layout = QVBoxLayout(res_group)
        self.decode_msg_output = QTextEdit()
        self.decode_msg_output.setReadOnly(True)
        res_layout.addWidget(self.decode_msg_output)
        
        self.copy_btn = QPushButton("Salin ke Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        res_layout.addWidget(self.copy_btn)
        
        right_panel.addWidget(res_group)
        layout.addLayout(right_panel, 1)

        return tab

    # UI Handlers
    def toggle_pass_visibility(self, line_edit):
        if line_edit.echoMode() == QLineEdit.EchoMode.Password:
            line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.EchoMode.Password)

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar", "", "PNG Images (*.png)")
        if file_path:
            self.current_img_path = file_path
            if self.tabs.currentIndex() == 0:
                self.encode_drop_area.set_image(file_path)
            else:
                self.decode_drop_area.set_image(file_path)

    def handle_file_dropped(self, file_path):
        if file_path.lower().endswith('.png'):
            self.current_img_path = file_path
            if self.tabs.currentIndex() == 0:
                self.encode_drop_area.set_image(file_path)
            else:
                self.decode_drop_area.set_image(file_path)
        else:
            QMessageBox.warning(self, "Format Salah", "Hanya mendukung file PNG.")

    def copy_to_clipboard(self):
        text = self.decode_msg_output.toPlainText()
        if text:
            pyperclip.copy(text)
            self.status_label.setText("Berhasil disalin ke clipboard!")

    # Processing
    def start_encode(self):
        if not self.current_img_path or not self.encode_msg_input.toPlainText() or not self.encode_pass_input.text():
            QMessageBox.warning(self, "Input Kurang", "Mohon lengkapi semua field.")
            return

        out_path, _ = QFileDialog.getSaveFileName(self, "Simpan Hasil Steganografi", "stego_result.png", "PNG Images (*.png)")
        if not out_path:
            return

        self.set_ui_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Sedang memproses enkripsi & encoding...")

        self.worker = WorkerThread(
            "encode",
            img_path=self.current_img_path,
            message=self.encode_msg_input.toPlainText(),
            password=self.encode_pass_input.text(),
            out_path=out_path
        )
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_encode_finished)
        self.worker.start()

    def on_encode_finished(self, success, result):
        self.set_ui_enabled(True)
        self.progress_bar.setVisible(False)
        if success:
            QMessageBox.information(self, "Sukses", f"Pesan berhasil disembunyikan!\nLokasi: {result}")
            self.status_label.setText("Encoding selesai.")
        else:
            QMessageBox.critical(self, "Gagal", f"Terjadi kesalahan: {result}")
            self.status_label.setText("Gagal.")

    def start_decode(self):
        if not self.current_img_path or not self.decode_pass_input.text():
            QMessageBox.warning(self, "Input Kurang", "Mohon pilih gambar dan masukkan password.")
            return

        self.set_ui_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Sedang mengekstrak pesan...")

        self.worker = WorkerThread(
            "decode",
            img_path=self.current_img_path,
            password=self.decode_pass_input.text()
        )
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_decode_finished)
        self.worker.start()

    def on_decode_finished(self, success, result):
        self.set_ui_enabled(True)
        self.progress_bar.setVisible(False)
        if success:
            self.decode_msg_output.setText(result)
            self.status_label.setText("Pesan berhasil diekstrak.")
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal mengekstrak: {result}")
            self.status_label.setText("Gagal.")

    def set_ui_enabled(self, enabled):
        self.tabs.setEnabled(enabled)
        self.encode_btn.setEnabled(enabled)
        self.decode_btn.setEnabled(enabled)

    def toggle_theme(self):
        from src.gui.styles import LIGHT_STYLE
        if self.current_theme == "dark":
            # Just a placeholder for light style since I only defined dark fully
            # I will improve the LIGHT_STYLE in styles.py next
            # self.setStyleSheet(LIGHT_STYLE)
            # self.theme_btn.setText("☀️ Light Mode")
            # self.current_theme = "light"
            pass # Keep dark for now as it looks best
        else:
            self.setStyleSheet(DARK_STYLE)
            self.theme_btn.setText("🌙 Dark Mode")
            self.current_theme = "dark"
