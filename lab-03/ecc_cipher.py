import sys
import os
import requests

# Set QT_QPA_PLATFORM_PLUGIN_PATH
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(__file__), 'platforms')

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ecc import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)
        
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

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, "Success", data.get("message", "Keys generated successfully!"))
            else:
                QMessageBox.critical(self, "Error", f"API error: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to API: {str(e)}")

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_signature.setPlainText(data.get("signature", ""))
                QMessageBox.information(self, "Success", "Signed Successfully")
            else:
                QMessageBox.critical(self, "Error", f"API error: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to API: {str(e)}")

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_signature.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get("is_verified", False):
                    QMessageBox.information(self, "Success", "Verified Successfully")
                else:
                    QMessageBox.warning(self, "Failure", "Verification Failed")
            else:
                QMessageBox.critical(self, "Error", f"API error: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to API: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
