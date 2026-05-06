DARK_STYLE = """
QMainWindow {
    background-color: #0f172a;
    color: #f8fafc;
}

QWidget {
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}

QTabWidget::pane {
    border: 1px solid #1e293b;
    background: #0f172a;
    border-radius: 8px;
    top: -1px;
}

QTabBar::tab {
    background: #1e293b;
    color: #94a3b8;
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: #3b82f6;
    color: white;
    font-weight: bold;
}

QGroupBox {
    border: 1px solid #1e293b;
    border-radius: 12px;
    margin-top: 20px;
    padding-top: 15px;
    background-color: #1e293b66;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #3b82f6;
    font-weight: bold;
}

QLineEdit, QTextEdit {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px;
    color: #f8fafc;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #3b82f6;
}

QPushButton {
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
}

QPushButton:hover {
    background-color: #2563eb;
}

QPushButton:pressed {
    background-color: #1d4ed8;
}

QPushButton#secondaryBtn {
    background-color: #334155;
}

QPushButton#secondaryBtn:hover {
    background-color: #475569;
}

QProgressBar {
    border: 1px solid #334155;
    border-radius: 5px;
    text-align: center;
    background-color: #1e293b;
    color: white;
}

QProgressBar::chunk {
    background-color: #3b82f6;
    width: 20px;
}

QLabel#previewArea {
    border: 2px dashed #334155;
    border-radius: 12px;
    background-color: #0f172a;
}

QLabel#previewArea:hover {
    border: 2px dashed #3b82f6;
}
"""

LIGHT_STYLE = """
/* Simplified light style for brevity, similar structure */
QMainWindow { background-color: #f8fafc; color: #0f172a; }
/* ... other components ... */
"""
