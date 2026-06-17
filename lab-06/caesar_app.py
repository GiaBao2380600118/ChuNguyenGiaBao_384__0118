import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, 
                             QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CaesarCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caesar Cipher - Lab 06")
        self.resize(550, 450)
        self.init_ui()
        self.apply_premium_styling()

    def init_ui(self):
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Title
        self.lbl_title = QLabel("CAESAR CIPHER TOOL")
        self.lbl_title.setObjectName("lbl_title")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_title)

        # Plaintext Label & Field
        self.lbl_plain = QLabel("Plain Text:")
        self.layout.addWidget(self.lbl_plain)
        self.txt_plain_text = QPlainTextEdit()
        self.txt_plain_text.setPlaceholderText("Enter text to encrypt here...")
        self.layout.addWidget(self.txt_plain_text)

        # Key Horizontal Layout
        self.key_layout = QHBoxLayout()
        self.lbl_key = QLabel("Shift Key (Integer):")
        self.txt_key = QLineEdit()
        self.txt_key.setPlaceholderText("e.g. 3")
        self.key_layout.addWidget(self.lbl_key)
        self.key_layout.addWidget(self.txt_key)
        self.layout.addLayout(self.key_layout)

        # Ciphertext Label & Field
        self.lbl_cipher = QLabel("Cipher Text:")
        self.layout.addWidget(self.lbl_cipher)
        self.txt_cipher_text = QPlainTextEdit()
        self.txt_cipher_text.setPlaceholderText("Enter text to decrypt here...")
        self.layout.addWidget(self.txt_cipher_text)

        # Action Buttons Layout
        self.btn_layout = QHBoxLayout()
        self.btn_encrypt = QPushButton("Encrypt")
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_layout.addWidget(self.btn_encrypt)

        self.btn_decrypt = QPushButton("Decrypt")
        self.btn_decrypt.clicked.connect(self.handle_decrypt)
        self.btn_layout.addWidget(self.btn_decrypt)

        self.layout.addLayout(self.btn_layout)

    def apply_premium_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121214;
            }
            QLabel {
                color: #E2E2E6;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                font-weight: 500;
            }
            QLabel#lbl_title {
                color: #9089FC;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
                letter-spacing: 1px;
            }
            QPlainTextEdit, QLineEdit {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #2A2A32;
                border-radius: 8px;
                padding: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
            }
            QPlainTextEdit:focus, QLineEdit:focus {
                border: 1px solid #9089FC;
            }
            QPushButton {
                background-color: #9089FC;
                color: #121214;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #A59FFA;
            }
            QPushButton:pressed {
                background-color: #7B73F0;
            }
        """)

    def caesar_cipher(self, text, shift, encrypt=True):
        if not text:
            return ""
        if not encrypt:
            shift = -shift
            
        result = []
        for char in text:
            if char.isupper():
                result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            elif char.islower():
                result.append(chr((ord(char) - 97 + shift) % 26 + 97))
            else:
                result.append(char)
        return "".join(result)

    def handle_encrypt(self):
        plain_text = self.txt_plain_text.toPlainText()
        key_str = self.txt_key.text().strip()
        if not key_str:
            QMessageBox.warning(self, "Input Error", "Please enter a shift key.")
            return
        try:
            shift = int(key_str)
        except ValueError:
            QMessageBox.warning(self, "Invalid Key", "Shift key must be an integer.")
            return

        cipher_text = self.caesar_cipher(plain_text, shift, encrypt=True)
        self.txt_cipher_text.setPlainText(cipher_text)

    def handle_decrypt(self):
        cipher_text = self.txt_cipher_text.toPlainText()
        key_str = self.txt_key.text().strip()
        if not key_str:
            QMessageBox.warning(self, "Input Error", "Please enter a shift key.")
            return
        try:
            shift = int(key_str)
        except ValueError:
            QMessageBox.warning(self, "Invalid Key", "Shift key must be an integer.")
            return

        plain_text = self.caesar_cipher(cipher_text, shift, encrypt=False)
        self.txt_plain_text.setPlainText(plain_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarCipherApp()
    window.show()
    sys.exit(app.exec_())
