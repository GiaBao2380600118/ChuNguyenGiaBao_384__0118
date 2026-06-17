import sys
import os

# Set QT_QPA_PLATFORM_PLUGIN_PATH
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(__file__), 'platforms')

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from signatures_q2 import Ui_MainWindow

from cipher.rsa.rsa_cipher import RSACipher
from cipher.ecc.ecc_cipher import ECCCipher

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Instantiate local cryptosystems
        self.rsa_cipher = RSACipher()
        self.ecc_cipher = ECCCipher()
        
        # Connect RSA Buttons
        self.ui.btn_rsa_gen.clicked.connect(self.rsa_gen_keys)
        self.ui.btn_rsa_sign.clicked.connect(self.rsa_sign)
        self.ui.btn_rsa_verify.clicked.connect(self.rsa_verify)
        
        # Connect ECC Buttons
        self.ui.btn_ecc_gen.clicked.connect(self.ecc_gen_keys)
        self.ui.btn_ecc_sign.clicked.connect(self.ecc_sign)
        self.ui.btn_ecc_verify.clicked.connect(self.ecc_verify)
        
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
            QGroupBox {
                border: 1px solid #2A2A32;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                color: #9089FC;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 8px;
                padding: 0 4px;
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

    # RSA Operations
    def rsa_gen_keys(self):
        try:
            msg = self.rsa_cipher.generate_keys()
            QMessageBox.information(self, "RSA Keys", msg)
        except Exception as e:
            QMessageBox.critical(self, "RSA Error", f"Failed to generate keys: {str(e)}")

    def rsa_sign(self):
        message = self.ui.txt_rsa_msg.toPlainText()
        try:
            private_key, _ = self.rsa_cipher.load_keys()
            sig_bytes = self.rsa_cipher.sign(message, private_key)
            self.ui.txt_rsa_sig.setPlainText(sig_bytes.hex())
            QMessageBox.information(self, "RSA Sign", "Message signed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "RSA Error", f"Failed to sign: {str(e)}")

    def rsa_verify(self):
        message = self.ui.txt_rsa_msg.toPlainText()
        sig_hex = self.ui.txt_rsa_sig.toPlainText().strip()
        if not sig_hex:
            QMessageBox.warning(self, "Input Error", "Please provide a signature to verify.")
            return
        try:
            _, public_key = self.rsa_cipher.load_keys()
            sig_bytes = bytes.fromhex(sig_hex)
            is_valid = self.rsa_cipher.verify(message, sig_bytes, public_key)
            if is_valid:
                QMessageBox.information(self, "RSA Verification", "Signature is VALID!")
            else:
                QMessageBox.warning(self, "RSA Verification", "Signature is INVALID!")
        except Exception as e:
            QMessageBox.critical(self, "RSA Error", f"Verification failed: {str(e)}")

    # ECC Operations
    def ecc_gen_keys(self):
        try:
            msg = self.ecc_cipher.generate_keys()
            QMessageBox.information(self, "ECC Keys", msg)
        except Exception as e:
            QMessageBox.critical(self, "ECC Error", f"Failed to generate keys: {str(e)}")

    def ecc_sign(self):
        message = self.ui.txt_ecc_msg.toPlainText()
        try:
            private_key, _ = self.ecc_cipher.load_keys()
            sig_bytes = self.ecc_cipher.sign(message, private_key)
            self.ui.txt_ecc_sig.setPlainText(sig_bytes.hex())
            QMessageBox.information(self, "ECC Sign", "Message signed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "ECC Error", f"Failed to sign: {str(e)}")

    def ecc_verify(self):
        message = self.ui.txt_ecc_msg.toPlainText()
        sig_hex = self.ui.txt_ecc_sig.toPlainText().strip()
        if not sig_hex:
            QMessageBox.warning(self, "Input Error", "Please provide a signature to verify.")
            return
        try:
            _, public_key = self.ecc_cipher.load_keys()
            sig_bytes = bytes.fromhex(sig_hex)
            is_valid = self.ecc_cipher.verify(message, sig_bytes, public_key)
            if is_valid:
                QMessageBox.information(self, "ECC Verification", "Signature is VALID!")
            else:
                QMessageBox.warning(self, "ECC Verification", "Signature is INVALID!")
        except Exception as e:
            QMessageBox.critical(self, "ECC Error", f"Verification failed: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
