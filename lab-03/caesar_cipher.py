import sys
import os
import requests

# Set QT_QPA_PLATFORM_PLUGIN_PATH
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(__file__), 'platforms')

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from caesar import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        
        # Apply premium stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121214;
            }
            QLabel {
                color: #E2E2E6;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QLabel#label_title {
                color: #9089FC;
                font-size: 20px;
                font-weight: bold;
                margin: 10px;
            }
            QPlainTextEdit, QLineEdit {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #2A2A32;
                border-radius: 6px;
                padding: 6px;
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
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #A59FFA;
            }
            QPushButton:pressed {
                background-color: #7B73F0;
            }
        """)
        
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        key_text = self.ui.txt_key.text()
        try:
            key = int(key_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Key", "Key must be an integer!")
            return
            
        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data.get("cipher_text", ""))
                QMessageBox.information(self, "Success", "Encrypted Successfully")
            else:
                QMessageBox.critical(self, "Error", f"API error: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to API: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        key_text = self.ui.txt_key.text()
        try:
            key = int(key_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Key", "Key must be an integer!")
            return
            
        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data.get("plain_text", ""))
                QMessageBox.information(self, "Success", "Decrypted Successfully")
            else:
                QMessageBox.critical(self, "Error", f"API error: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to API: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
